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
        first_name (str): User's first name
        last_name (str): User's last name
        icon (str, optional): Name of the file with user's avatar.
    """
    email = models.EmailField(max_length=50, unique=True)
    first_name = models.CharField(blank=True, max_length=30)
    last_name = models.CharField(blank=True, max_length=20)
    icon = models.CharField(blank=True, max_length=30)

    objects = BaseUserManager()
    USERNAME_FIELD = 'email'

    def __str__(self):
        """
        :return: All the information about user which is added.
        """
        return str(self.to_dict())[:]

    def __repr__(self):
        """
        :return: Basic information which includes user id and email.
        """
        return f"id:{self.id} email:{self.email}"

    def to_dict(self):
        """
        Convert information which added user to dictionary where
        key is description of added information and value is an information.
        """
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
        }

    def update(self, password, first_name=None, last_name=None, icon=None):
        """
        Method which changes an information except email as it is an id of an user.
        """
        self.first_name = first_name if first_name else ""
        self.last_name = last_name if last_name else ""
        self.icon = icon if icon else ""

        if password:
            self.set_password(password)
        self.save()

    @classmethod
    def create(cls, email, password, first_name=None, last_name=None, icon=None):
        """
        Class method which creates user. Email and password are obligatory.
        """
        data = {}
        data["email"] = email
        data["first_name"] = first_name if first_name else ""
        data["last_name"] = last_name if last_name else ""
        data["icon"] = icon if icon else ""
        user = cls(**data)
        user.set_password(password)
        try:
            user.save()
            return user
        except (ValueError, AttributeError):
            pass

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
