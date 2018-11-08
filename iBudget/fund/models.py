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
            is_active(bool): "True" if this fund category exist, "false" in other way.

    """
    name = models.CharField(max_length=30)
    icon = models.CharField(max_length=30)
    is_shared = models.BooleanField(default=False)
    owner = models.ForeignKey(UserProfile, on_delete=True)
    is_active = models.BooleanField(default=True)

    def update(self, name=None, icon=None, is_shared=None, is_active=None):
        """
        Method which changes an information.
        """
        if name:
            self.name = name
        if icon:
            self.icon = icon
        if is_shared is not None:
            self.is_shared = is_shared
        if is_active is not None:
            self.is_active = is_active
        try:
            self.save()
        except (ValueError, AttributeError):
            pass

    @staticmethod
    def filter_by_user(user, is_shared=False, is_active=True):
        """
        Args:
            user (FK): user of fund,
            is_shared(bool): which category we need(shared or not shared).
            is_active(bool): 'True' if fund category exist
        Returns:
            FundCategories object if database contain fund for user
            and is_shared value, None otherwise.

        """
        return FundCategories.objects.filter(owner=user, is_shared=is_shared, is_active=is_active)


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

    def update(self, value=None, start_date=None, finish_date=None, fund=None):
        """
        Method which changes an information.
        """
        if value:
            self.value = value
        if start_date:
            self.start_date = start_date
        if finish_date:
            self.finish_date = finish_date
        if fund:
            self.fund = fund
        self.save()

    @staticmethod
    def filter_by_data(value, start_date, finish_date, fund):
        """
        Args:
            value: financial aim.
            fund: Fund for individual purpose.
            start_date: The beginning of time period.
            finish_date: The end of time period.
        Returns:
            SpendingLimitationIndividual object if row with described data exists, None otherwise.


        """
        goals = FinancialGoal.objects.filter(
            value=value,
            start_date=start_date,
            finish_date=finish_date,
            fund=fund)
        return goals

    @staticmethod
    def has_goals(fund_id):
        """
        Args:
            fund_id(int): Current session fund`s id.
        Returns:
            'True' if goal exist, and return 'False' if it is not.

        """
        return FinancialGoal.objects.filter(fund=fund_id).exists()

    @staticmethod
    def get_by_id(goal_id):
        """
            Args:
                goal_id(int): index of goal category.
            Returns:
                FinancialGoal object if database contain goal with id, None otherwise.

        """
        try:
            return FinancialGoal.objects.get(pk=goal_id)
        except (FundCategories.DoesNotExist, ValueError):
            return None
