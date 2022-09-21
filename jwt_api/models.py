from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        """  create and return user with username, email, password  """
        if username is None:
            raise TypeError('Пользователь должен содержать username')

        if email is None:
            raise TypeError('Пользователь должен содержать email')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password):
        """ create and return superuser """
        if password is None:
            raise TypeError('Админ должен иметь пароль')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractUser, PermissionsMixin):
    name = models.CharField(max_length=255, db_index=True, unique=True)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    # если хотим сохранить в refresh_token в бд:
    # refresh = models.CharField(max_length=512, unique=True, default=None)

    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return str(self.name) + str(self.id)
