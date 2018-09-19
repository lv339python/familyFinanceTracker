from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class UserProfile(AbstractBaseUser):
    """A user's profile.

    Attributes:
        email (str): User's email.
        password (str): User's password.
        icon (str, optional): Name of the file with user's avatar.

    """
    email = models.EmailField(max_length=50, unique=True)
    icon = models.CharField(max_length=30)

    objects = BaseUserManager()
    USERNAME_FIELD = 'email'

