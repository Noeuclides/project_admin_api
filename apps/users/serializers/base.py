from apps.users.models import User
from django.contrib.auth import password_validation
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


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


class UserPasswordChangeSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=8, max_length=64)
    new_password = serializers.CharField(min_length=8, max_length=64)
    confirm_new_password = serializers.CharField(min_length=8, max_length=64)

    def validate(self, data):
        """Check credentials.
        """
        if data['new_password'] == data['password']:
            raise serializers.ValidationError('Password must be different')
        if data['new_password'] != data['confirm_new_password']:
            raise serializers.ValidationError('New passwords does not match.')
        self.context['new_password'] = data['new_password']
        return data

    def update(self, user):
        user.password = self.context.get('new_password')
        user.save()
