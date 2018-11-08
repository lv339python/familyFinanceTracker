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
            is_active(bool): "True" if this income history exist, "false" in other way.

    """
    income = models.ForeignKey(IncomeCategories, on_delete=True, related_name="income_history")
    fund = models.ForeignKey(FundCategories, on_delete=True, related_name="income_history")
    date = models.DateTimeField()
    value = models.DecimalField(max_digits=17, decimal_places=2)
    comment = models.TextField(null=True, default="")
    is_active = models.BooleanField(default=True)

    def update(self, income=None, fund=None, date=None, value=None, comment=None, is_active=None):
        """
        Method which changes an information.
        """

        if income:
            self.income = income
        if fund:
            self.fund = fund
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
        except (ValueError, AttributeError):
            pass

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

