"""
This module provides user profile  model.
"""

from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.db import models


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

    @staticmethod
    def get_by_email(email):
        """
        Args:
            email(str): The first parameter.
        Returns:
            UserProfile object if database contain user with email, None otherwise.

        """

        try:
            user = UserProfile.objects.get(email=email)
            return user
        except UserProfile.DoesNotExist:
            return None
