from django.conf import settings
from django.contrib.auth import authenticate, password_validation
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator

from apps.users.models import User


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'name',
            'last_name',
            'password',
        ]


class UserRegisterSerializer(serializers.Serializer):
    """
    User sign up serializer.
    Handle sign up data validation and user creation.
    """

    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        min_length=4,
        max_length=20,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(min_length=8, max_length=64)
    password_confirmation = serializers.CharField(min_length=8, max_length=64)

    name = serializers.CharField(min_length=2, max_length=30)
    last_name = serializers.CharField(min_length=2, max_length=30)

    def validate(self, data):
        """
        Verify passwords match.
        """
        password = data['password']
        password_confirmaton = data['password_confirmation']
        if password != password_confirmaton:
            raise serializers.ValidationError("Passwords don't match.")
        password_validation.validate_password(password)
        return data

    def create(self, data):
        """
        Handle user creation.
        """
        data.pop('password_confirmation')
        user = User.objects.create_user(**data)
        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()

    # Password
    password = serializers.CharField(min_length=8, max_length=64)

    def validate(self, data):
        """Check credentials.
        """
        user = authenticate(
            username=data['username'],
            password=data['password']
        )
        if not user:
            raise serializers.ValidationError('Invalid credentials')
        if not user.is_enabled:
            raise serializers.ValidationError('Account is not active yet')
        self.context['user'] = user
        return data

    def create(self, data):
        """
        Generate or retrieve new token.
        """
        token, _ = Token.objects.get_or_create(user=self.context['user'])
        return self.context['user'], token.key
