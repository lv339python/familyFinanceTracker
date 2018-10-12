"""
This module provides model of fund category.
"""

from django.db import models

from authentication.models import UserProfile


class FundCategories(models.Model):
    """Categories of available user's funds.

        Attributes:
            name (str): Category name.
            icon (str, optional): Name of the file with category's avatar.
            is_shared (bool):  "True" if this fund category is shared, "false" in other way.
            owner (FK): Owner of this fund category.

    """
    name = models.CharField(max_length=30)
    icon = models.CharField(max_length=30)
    is_shared = models.BooleanField(default=False)
    owner = models.ForeignKey(UserProfile, on_delete=True)

    @staticmethod
    def filter_by_user(user, is_shared=False):
        """
        Args:
            user (FK): user of fund,
            is_shared(bool): which category we need(shared or not shared).
        Returns:
            FundCategories object if database contain fund for user
            and is_shared value, None otherwise.

        """
        return FundCategories.objects.filter(owner=user, is_shared=is_shared)

    @staticmethod
    def get_by_id(fund_id):
        """
            Args:
                fund_id(int): index of fund category.
            Returns:
                FundCategories object if database contain fund with id, None otherwise.

        """
        try:
            return FundCategories.objects.get(pk=fund_id)
        except (FundCategories.DoesNotExist, ValueError):
            return None


class FinancialGoal(models.Model):
    """
    Categories of available user's financial goal.
        Attributes:
        value (decimal):  Goal value.
        start_date(Date): Date when goal was set.
        finish_date(Date): Date when goal should be reached.
        fund (FK): Fund for this goal.

    """
    value = models.DecimalField(max_digits=17, decimal_places=2)
    start_date = models.DateField()
    finish_date = models.DateField()
    fund = models.OneToOneField(
        FundCategories,
        on_delete=models.CASCADE,
        related_name="goal"
    )
