"""
This module provides models of spending category and spending limitation.
"""

from django.db import models

from authentication.models import UserProfile


class SpendingCategories(models.Model):
    """Categories of user's spending.

      Attributes:
          name (str): Name of user's spending.
          icon (str, optional): Name of the file with  spending's avatar.
          owner (FK): Owner of this category.
          is_shared (bool):  "True" if this spending category is shared, "false" in other way.
          is_active(bool): "True" if this spending category exist, "false" in other way.


    """
    name = models.CharField(max_length=30)
    icon = models.CharField(max_length=30)
    owner = models.ForeignKey(UserProfile, on_delete=True)
    is_shared = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    @staticmethod
    def get_by_id(spending_category_id):
        """
        Args:
            spending_category_id (int): The first parameter.
        Returns:
            SpendingCategories object if database contain spending
            category with id, None otherwise.

        """
        try:
            return SpendingCategories.objects.get(pk=spending_category_id)
        except (SpendingCategories.DoesNotExist, ValueError):
            return None

    @staticmethod
    def filter_by_id(spending_category_id, is_active=True):
        """
        Args:
            spending_category_id (int): The first parameter.
            is_active(bool): which category is active.
        Returns:
            SpendingCategories object if database contain spending
            category with id, None otherwise.

        """
        return SpendingCategories.objects.filter(pk=spending_category_id, is_active=is_active)

    @staticmethod
    def filter_by_user(user, is_shared=False, is_active=True):
        """
        Args:
            user (UserProfile): user of category,
            is_shared(bool): which category we need(shared or not shared).
            is_active(bool): which category is active.
        Returns:
            SpendingCategories object if database contain category for this user
            and is_shared value, None otherwise.
        """
        return SpendingCategories.objects.filter(owner=user,
                                                 is_shared=is_shared,
                                                 is_active=is_active)

    @staticmethod
    def filter_by_owner_name(owner, name, is_active=True):
        """
        Args:
            owner (UserProfile): owner of category,
            name(bool): name of category.
            is_active(bool): which category is active.
        Returns:
            SpendingCategories object if database contain category for this user
            and name, None otherwise.
        """
        return SpendingCategories.objects.filter(owner=owner, name=name, is_active=is_active)


class SpendingLimitationIndividual(models.Model):
    """Limitation of user's spending.

        Attributes:
            user (FK): Id of user profile.
            spending_category (FK): Id of spending category.
            start_date (date): The beginning of limitation period.
            finish_date (date): The ending of limitation period.
            value (decimal): Value of limitation.


    """
    user = models.ForeignKey(UserProfile, on_delete=True)
    spending_category = models.ForeignKey(SpendingCategories, on_delete=True)
    start_date = models.DateField()
    finish_date = models.DateField()
    value = models.DecimalField(max_digits=17, decimal_places=2)

    @staticmethod
    def filter_by_data(user, spending_category, start_date, finish_date):
        """
        Args:
            user (FK): Owner of this category.
            spending_category (FK): Spending category for individual purpose.
            start_date: The beginning of time period.
            finish_date: The end of time period.
        Returns:
            SpendingLimitationIndividual object if row with described data exists, None otherwise.


        """
        notice = SpendingLimitationIndividual.objects.filter(
            user=user,
            spending_category=spending_category,
            start_date=start_date,
            finish_date=finish_date)
        return notice

    @staticmethod
    def get_value_by_data(user, spending_category, start_date, finish_date):
        """
        Args:
            user (FK): Owner of this category.
            spending_category (FK): Spending category for individual purpose.
            start_date: The beginning of time period.
            finish_date: The end of time period.
        Returns:
            Limit value if such exists, 0 otherwise.


        """
        return sum(SpendingLimitationIndividual.objects.filter(
            user=user,
            spending_category=spending_category,
            start_date=start_date,
            finish_date=finish_date).values_list('value', flat=True))


class SpendingLimitationGroup(models.Model):
    """Limitation of group's spending.

        Attributes:
            spending_category (FK): Id of spending category.
            start_date (date): The beginning of limitation period.
            finish_date (date): The ending of limitation period.
            value (decimal): Value of limitation.


    """

    spending_category = models.ForeignKey(SpendingCategories, on_delete=True)
    start_date = models.DateField()
    end_date = models.DateField()
    value = models.DecimalField(max_digits=17, decimal_places=2)
