"""
This module provides model of income category.
"""

from django.db import models

from authentication.models import UserProfile


class IncomeCategories(models.Model):
    """Categories of user's income.

        Attributes:
            name (str): Name of user's income.
            date (date): Date of user's income.
            value (decimal): Value of user's income.
            icon (str, optional): Name of the file with income's avatar.
            owner (FK): ID owner of this category.
            is_active(bool): "True" if this income category exist, "false" in other way.


    """
    name = models.CharField(max_length=30)
    date = models.DateField()
    value = models.DecimalField(max_digits=17, decimal_places=2)
    icon = models.CharField(max_length=30)
    owner = models.ForeignKey(UserProfile, on_delete=True)
    is_active = models.BooleanField(default=True)

    def update(self, name=None, date=None, value=None, icon=None, is_active=None):
        """
        Method which changes an information.
        """

        if name:
            self.name = name
        if date:
            self.date = date
        if value is not None:
            self.value = value
        if icon:
            self.icon=icon
        if is_active is not None:
            self.is_active = is_active
        try:
            self.save()
        except (ValueError, AttributeError):
            pass


    @staticmethod
    def filter_by_user(user, is_active=True):
        """
        Args:
            user (UserProfile): user of category,
            is_active(bool): which income is active.
        Returns:
            SpendingCategories object if database contain category for this user
            and is_shared value, None otherwise.
        """
        return IncomeCategories.objects.filter(owner=user, is_active=is_active)

    @staticmethod
    def get_by_id(income_category_id):
        """
        Args:
            spending_category_id (int): The first parameter.
        Returns:
            SpendingCategories object if database contain spending
            category with id, None otherwise.

        """
        try:
            return IncomeCategories.objects.get(pk=income_category_id)
        except (IncomeCategories.DoesNotExist, ValueError):
            return None

    @staticmethod
    def filter_by_owner_name(owner, name, is_active=True):
        """
        Args:
            owner (UserProfile): owner of category,
            name(bool): name of category.
            is_active(bool): which income is active.
        Returns:
            IncomeCategories object if database contain category for this user
            and name, None otherwise.


        """
        return IncomeCategories.objects.filter(owner=owner, name=name, is_active=is_active)
