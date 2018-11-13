"""
This module provides model of income history.
"""
import datetime

from django.db import models

from fund.models import FundCategories
from income.models import IncomeCategories


class IncomeHistory(models.Model):
    """Data about transferring from income to fund.

        Attributes:
            income (FK): Income category ID.
            fund (FK): Fund category ID.
            date (date): Date of transfer.
            value (decimal): Value of transfer.
            comment (str, optional): Describing source of transfer.
            is_active(bool): "True" if this income history exist, "false" in other way.

    """
    income = models.ForeignKey(IncomeCategories, on_delete=True, related_name="income_history")
    fund = models.ForeignKey(FundCategories, on_delete=True, related_name="income_history")
    date = models.DateTimeField()
    value = models.DecimalField(max_digits=17, decimal_places=2)
    comment = models.TextField(null=True, default="")
    is_active = models.BooleanField(default=True)

    @staticmethod
    def get_by_id(income_history_id):
        """
        Args:
            income_history_id (int): The first parameter.
        Returns:
            IncomeHistory object if database contain income
            history category with id, None otherwise.
        """
        try:
            return IncomeHistory.objects.get(pk=income_history_id)
        except (IncomeHistory.DoesNotExist, ValueError):
            return None

    @staticmethod
    def filter_by_fund_id(fund_name, is_active=True):
        """
            Args:
                fund_name (int): The first parameter.
                is_active(bool): 'True' if IncomeHistory exist
            Returns:
                IncomeHistory objects if database contains history
                for this fund, None otherwise.

        """
        return IncomeHistory.objects.filter(pk=fund_name, is_active=is_active)

    @staticmethod
    def filter_by_user_date_spending(user,
                                     start_date,
                                     finish_date,
                                     income_categories=None,
                                     is_active=True):
        """
        Args:
            user (UserProfile): owner of transaction,
            start_date (date): The beginning of statistic period
            finish_date (date): The end of statistic period
            income_categories (IncomeCategories): income category
            is_active(bool): 'True' if spending history exist
        Returns:
            SpendingHistory objects if database contains such, None otherwise.

        """

        if income_categories:
            return IncomeHistory.objects.filter(owner=user,
                                                income_categories=income_categories,#pylint: disable=duplicate-code
                                                date__range=[start_date -
                                                             datetime.timedelta(days=1),
                                                             finish_date],
                                                is_active=is_active)
        total = 0
        for item in IncomeHistory.objects.filter(owner=user,#pylint: disable=duplicate-code
                                                 date__range=[start_date -
                                                              datetime.timedelta(days=1),
                                                              finish_date],
                                                 is_active=is_active):
            total += float(item.value)
        return total
