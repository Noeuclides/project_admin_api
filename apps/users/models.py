from __future__ import annotations

from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.validators import UnicodeUsernameValidator


class UserManager(BaseUserManager):
    def _create_user(
            self, username: str, email: str, name: str, last_name: str,
            password: str, is_staff: bool, is_superuser: bool,
            **extra_fields
    ) -> User:
        user = self.model(
            username=username,
            email=email,
            name=name,
            last_name=last_name,
            is_staff=is_staff,
            is_superuser=is_superuser,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(
            self, username: str, email: str, name: str,
            last_name: str, password: str = None, **extra_fields
    ) -> User:
        return self._create_user(
            username,
            email,
            name,
            last_name,
            password,
            False,
            False,
            **extra_fields)

    def create_superuser(
            self, username: str, email: str, name: str,
            last_name: str, password: str = None, **extra_fields
    ) -> User:
        return self._create_user(
            username,
            email,
            name,
            last_name,
            password,
            True,
            True,
            True,
            **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        'username',
        max_length=150,
        unique=True,
        help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
        validators=[username_validator],
        error_messages={
            'unique': "A user with that username already exists.",
        },
    )
    email = models.EmailField('email', max_length=255, unique=True)
    name = models.CharField('name', max_length=255)
    last_name = models.CharField('last name', max_length=255)
    is_enabled = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=True)
    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name', 'last_name', 'email']

    def __str__(self) -> str:
        return f'{self.username}'
