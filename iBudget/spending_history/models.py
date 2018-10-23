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

    @staticmethod
    def filter_by_user_date_spending(user,
                                     start_date,
                                     finish_date,
                                     spending_categories=None):
        """
        Args:
            user (UserProfile): owner of transaction,
            start_date (date): The beginning of statistic period
            finish_date (date): The end of statistic period
            spending_categories (SpendingCategories): spending category
        Returns:
            SpendingHistory objects if database contains such, None otherwise.


        """

        if spending_categories:
            return SpendingHistory.objects.filter(owner=user,
                                                  spending_categories=spending_categories,
                                                  date__range=[start_date -
                                                               datetime.timedelta(days=1),
                                                               finish_date])
        total = 0
        for item in SpendingHistory.objects.filter(owner=user,
                                                   date__range=[start_date -
                                                                datetime.timedelta(days=1),
                                                                finish_date]):
            total += float(item.value)
        return total
