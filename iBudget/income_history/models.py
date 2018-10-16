"""
This module provides model of income history.
"""

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

    """
    income = models.ForeignKey(IncomeCategories, on_delete=True, related_name="income_history")
    fund = models.ForeignKey(FundCategories, on_delete=True, related_name="income_history")
    date = models.DateTimeField()
    value = models.DecimalField(max_digits=17, decimal_places=2)
    comment = models.TextField(null=True, default="")

    @staticmethod
    def filter_by_fund_id(fund_name):
        return IncomeHistory.objects.filter(pk=fund_name)
