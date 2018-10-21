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

    """
    name = models.CharField(max_length=30)
    date = models.DateField()
    value = models.DecimalField(max_digits=17, decimal_places=2)
    icon = models.CharField(max_length=30)
    owner = models.ForeignKey(UserProfile, on_delete=True)


    @staticmethod
    def filter_by_user(user):
        """
        Args:
            user (UserProfile): user of category,
            is_shared(bool): which category we need(shared or not shared).
        Returns:
            SpendingCategories object if database contain category for this user
            and is_shared value, None otherwise.
        """
        return IncomeCategories.objects.filter(owner=user)

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
