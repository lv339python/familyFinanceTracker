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
    def filter_by_user_id(user_id, is_shared):
        """
        Args:
            user_id (int): index of user,
            is_shared(bool): which category we need(shared or not shared)
        Returns:
            FundCategories object if database contain category with user_id
            and is_shared value, None otherwise.
        """
        try:
            return FundCategories.objects.filter(owner=user_id,
                                                 is_shared=is_shared)
        except FundCategories.DoesNotExist:
            return None

    @staticmethod
    def get_by_id(fund_id):
        """
            Args:
                fund_id(int): index of fund category.
            Returns:
                FundCategories object if database contain fund with id, None otherwise.
        """
        try:
            return FundCategories.objects.get(id=fund_id)
        except FundCategories.DoesNotExist:
            return None
