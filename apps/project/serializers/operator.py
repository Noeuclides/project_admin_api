from datetime import timedelta

import jwt
from apps.users.models import User
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
from rest_framework import serializers

from .base import UserRegisterSerializer, UserModelSerializer


class OperatorRegisterSerializer(UserModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    # def update(self, instance, validated_data):
    #     instance.username = validated_data.get('username')
    #     instance.email = validated_data.get('email')
    #     instance.name = validated_data.get('name')
    #     instance.last_name = validated_data.get('last_name')
    #     instance.is_enabled = validated_data.get('is_enabled')
    #     instance.is_admin = validated_data.get('is_admin')
    #     instance.save()
    #     return instance

    # def create(self, data):
    #     data.pop('password_confirmation')
    #     user = User.objects.create_user(
    #         **data, is_enabled=False, is_admin=False
    #     )
    #     self.send_confirmation_email(user)
    #     return user

    def create(self, validated_data: dict) -> User:
        validated_data['is_enabled'] = False
        validated_data['is_admin'] = False
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        self.send_confirmation_email(user)
        return user

    def send_confirmation_email(self, user):
        """
        Send account verification link to new operator.
        """
        verification_token = self.generate_verification_token(user)
        subject = f'Welcome @{user.username}! Verify your account to create a project'
        from_email = 'Project Creator <noreply@projectcreator.com>'
        content = render_to_string(
            'users/account_verification.html',
            {'token': verification_token, 'user': user}
        )
        msg = EmailMultiAlternatives(
            subject, content, from_email, [user.email])
        msg.attach_alternative(content, "text/html")
        msg.send()

    def generate_verification_token(self, user):
        """
        Create JWT token that the operator can use to verify its account.
        """
        exp_date = timezone.now() + timedelta(days=3)
        payload = {
            'user': user.username,
            'exp': int(exp_date.timestamp()),
            'type': 'email_confirmation'
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        return token


class AccountVerificationSerializer(serializers.Serializer):
    """
    Account verification serializer.
    """

    token = serializers.CharField()

    def validate_token(self, data):
        """
        Verify token is valid.
        """
        try:
            payload = jwt.decode(data, settings.SECRET_KEY,
                                 algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise serializers.ValidationError('Verification link has expired.')
        except jwt.PyJWTError:
            raise serializers.ValidationError('Invalid token')
        if payload['type'] != 'email_confirmation':
            raise serializers.ValidationError('Invalid token')

        self.context['payload'] = payload
        return data

    def save(self):
        """
        Update operator enabled status to be able to login.
        """
        payload = self.context['payload']
        user = User.objects.get(username=payload['user'])
        user.is_enabled = True
        user.save()
