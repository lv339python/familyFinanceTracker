"""
This module provides model of spending category.
"""
from django.contrib.auth.base_user import BaseUserManager
from django.db import models

from authentication.models import UserProfile


class SpendingCategories(models.Model):
    """Categories of user's spending.

        Attributes:
            name (str): Name of user's spending.
            icon (str, optional): Name of the file with  spending's avatar.
            owner (FK): Owner of this category.
            is_shared (bool):  "True" if this spending category is shared, "false" in other way.


    """
    name = models.CharField(max_length=30)
    icon = models.CharField(max_length=30)
    owner = models.ForeignKey(UserProfile, on_delete=True)
    is_shared = models.BooleanField(default=False)
    objects = BaseUserManager()

    def __str__(self):
        """
        :return: All the information about categories spending which is added.
        """
        return str(self.to_dict())[:]

    def __repr__(self):
        """
        :return: Basic information which includes categories spending.
        """
        return f"id:{self.id} name:{self.name}"

    def to_dict(self):
        """
        Convert information which added spendings to dictionary where
        key is description of added information and value is an information.
        """
        return {
            'id': self.id,
            'name': self.name,
            'icon': self.icon,
            'owner': self.owner,
            'is_shared':self.is_shared,
        }

    def update(self, name, owner, icon=None, is_shared=None):
        """
        Method which changes an information except owner as it is an id of an user.
        """

        if name:
          self.name = name
        if icon:
          self.icon = icon
        if owner:
          self.owner = owner
        if is_shared:
          self.is_shared = is_shared
        self.save()

    @classmethod
    def create(cls, name, icon=None, owner=None, is_shared=None):
        """
        Class method which creates categories of spending.
        """
        data = {}
        data["name"] = name
        data["icon"] = icon if icon else ""
        data["owner"] = owner if owner else ""
        data["is_shared"] = is_shared if is_shared else ""
        spending_categories = cls(**data)

        try:
            spending_categories.save()
            return spending_categories
        except (ValueError, AttributeError):
            pass

    @staticmethod
    def get_by_name(name):
        """
        Args:
            name(str): The first parameter.
        Returns:
            SpendingCategories object if database contain user with spending categories, None otherwise.

        """

        try:
            spending_categories = SpendingCategories.objects.get(name=name)
            return spending_categories
        except SpendingCategories.DoesNotExist:
            return None

    @staticmethod
    def get_by_spend_id(spending_categories_id):

      """
      returns object of Spending category by id
      """

      try:
        spending_categories = SpendingCategories.objects.get(id=spending_categories_id)
        return spending_categories
      except SpendingCategories.DoesNotExist:
        return None


    @staticmethod
    def get_category(request, name):

      """
      returns users category by user_id and name
      """

      try:
        spending_category = SpendingCategories.objects.get(owner=request.user, name=name)
        return spending_category
      except SpendingCategories.DoesNotExist:
        return None


    @staticmethod
    def set_shared(user_id, spending_categories_id):

      """
      returns object of Group by id
      """

      try:
        spending_categories = SpendingCategories.objects.set(user_id=user_id, id=spending_categories_id)
        return spending_categories
      except SpendingCategories.DoesNotExist:
        return None
