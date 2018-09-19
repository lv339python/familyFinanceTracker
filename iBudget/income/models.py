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
