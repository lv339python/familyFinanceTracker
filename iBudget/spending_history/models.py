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
            is_active (bool): "True" if this spending history exist, "false" in other way.

    """
    fund = models.ForeignKey(FundCategories, on_delete=True, related_name="spending_history")
    spending_categories = models.ForeignKey(SpendingCategories,
                                            on_delete=True,
                                            related_name="spending_history")
    date = models.DateTimeField()
    value = models.DecimalField(max_digits=17, decimal_places=2)
    owner = models.ForeignKey(UserProfile, on_delete=True)
    comment = models.TextField(null=True, default="")
    is_active = models.BooleanField(default=True)

    def update(self, fund=None, spending_categories=None, date=None, value=None, comment=None, is_active=None):
        """
        Method which changes an information.
        """
        if fund:
            self.fund = fund
        if spending_categories:
            self.spending_categories = spending_categories
        if date:
            self.date = date
        if value:
            self.value = value
        if comment:
            self.comment = comment
        if is_active is not None:
            self.is_active = is_active
        try:
            self.save()
        except(ValueError, AttributeError):
            pass

    @staticmethod
    def get_by_id(spending_history_id):
        """
        Args:
            spending_history_id (int): The first parameter.
        Returns:
            SpendingHistory object if database contain spending
            history category with id, None otherwise.
        """
        try:
            return SpendingHistory.objects.get(pk=spending_history_id)
        except (SpendingHistory.DoesNotExist, ValueError):
            return None

    @staticmethod
    def filter_by_user_date_spending(user,
                                     start_date,
                                     finish_date,
                                     spending_categories=None,
                                     is_active=True):
        """
        Args:
            user (UserProfile): owner of transaction,
            start_date (date): The beginning of statistic period
            finish_date (date): The end of statistic period
            spending_categories (SpendingCategories): spending category
            is_active(bool): 'True' if spending history exist
        Returns:
            SpendingHistory objects if database contains such, None otherwise.


        """

        if spending_categories:
            return SpendingHistory.objects.filter(owner=user,
                                                  spending_categories=spending_categories,
                                                  date__range=[start_date -
                                                               datetime.timedelta(days=1),
                                                               finish_date],
                                                  is_active=is_active)
        total = 0
        for item in SpendingHistory.objects.filter(owner=user,
                                                   date__range=[start_date -
                                                                datetime.timedelta(days=1),
                                                                finish_date],
                                                   is_active=is_active):
            total += float(item.value)
        return total

    @staticmethod
    def filter_by_user_date(user, start_date, finish_date, is_active=True):
        """
        Args:
            user (UserProfile): owner of transaction,
            start_date (date): The beginning of statistic period
            finish_date (date): The end of statistic period
            is_active(bool): 'True' if spending history exist
        Returns:
            SpendingHistory objects if database contains such, None otherwise.


        """
        return SpendingHistory.objects.filter(owner=user,
                                              date__range=[start_date - datetime.timedelta(days=1),
                                                           finish_date],
                                              is_active=is_active)

    @staticmethod
    def filter_by_user(user, is_active=True):
        """
        Args:
            user (UserProfile): user of category,
            is_active(bool): 'True' if spending history exist

        Returns:
            SpendingCategories object if database contain category for this user
            and is_shared value, None otherwise.

        """
        return SpendingHistory.objects.filter(owner=user, is_active=is_active)
