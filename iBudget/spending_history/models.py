"""
This module provides model of spending history.
"""

from django.db import models

from authentication.models import UserProfile
from fund.models import FundCategories
from spending.models import SpendingCategories


class SpendingHistory(models.Model):
    """Data about transferring from fund to spending.

        Attributes:
            fund (FK): Fund category ID.
            spending_categories (FK): Spending category ID.
            date (date): Date of transfer.
            value (decimal): Value of transfer.
            owner (FK): Owner of spending category.
            comment (str, optional): Describing of transfer.

    """
    fund = models.ForeignKey(FundCategories, on_delete=True, related_name="spending_history")
    spending_categories = models.ForeignKey(SpendingCategories,
                                            on_delete=True,
                                            related_name="spending_history")
    date = models.DateTimeField()
    value = models.DecimalField(max_digits=17, decimal_places=2)
    owner = models.ForeignKey(UserProfile, on_delete=True)
    comment = models.TextField(null=True, default="")
