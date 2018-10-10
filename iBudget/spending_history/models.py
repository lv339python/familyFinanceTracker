"""
This module provides model of spending history.
"""
import datetime

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

    @classmethod
    def create(cls, fund, spending_categories, owner, value, date, comment): #pylint: disable=too-many-arguments
        """
        Class method which creates spending history. All arguments are obligatory.
        """
        data = {}
        data["fund"] = fund if fund else ""
        data["spending_categories"] = spending_categories if spending_categories else ""
        data["date"] = date if date else datetime.datetime.now()
        data["value"] = value if value else ""
        data["owner"] = owner if owner else ""
        data["comment"] = comment if comment else ""
        spending = cls(**data)
        try:
            spending.save()
            return spending
        except (ValueError, AttributeError):
            pass
