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
        is_sys_admin (bool):  "True" if user has right of administrator, "False" in other way.
        one_time_token(HttpResponse): for deactivating update_password.
        is_fixed_period (bool): "True" if user chooses monthly/yearly limitation period,
            "False" in other way.
        is_active(bool): "True" if user exist, "false" in other way.
    """
    email = models.EmailField(max_length=50, unique=True)
    password = models.CharField(max_length=128)
    first_name = models.CharField(blank=True, max_length=30)
    last_name = models.CharField(blank=True, max_length=20)
    icon = models.CharField(blank=True, max_length=30)
    is_sys_admin = models.BooleanField(default=False)
    one_time_token = models.CharField(blank=True, max_length=255)
    ind_period_fixed = models.BooleanField(null=True)
    is_active = models.BooleanField(default=True)
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
            'is_sys_admin': self.is_sys_admin,
        }

    def update(self, password=None, one_time_token=None, first_name=None,
               last_name=None, icon=None, is_active=None):
        """
        Method which changes an information except email as it is an id of an user.
        """
        if first_name:
            self.first_name = first_name
        if icon:
            self.icon = icon
        if last_name:
            self.last_name = last_name
        if password:
            self.set_password(password)
        if one_time_token is not None:
            self.one_time_token = one_time_token
        if is_active is not None:
            self.is_active = is_active
        try:
            self.save()
        except(ValueError, AttributeError):
            pass

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

    @staticmethod
    def get_by_id(user_id):
        """
        Args:
            user_id (int): The first parameter.
        Returns:
            UserProfile object if database contain user with id, None otherwise.

        """

        try:
            user = UserProfile.objects.get(pk=user_id)
            return user
        except UserProfile.DoesNotExist:
            return None
