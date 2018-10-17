"""
This module provides model of group and its relations.
"""
from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from authentication.models import UserProfile
from fund.models import FundCategories
from spending.models import SpendingCategories


class Group(models.Model):
    """Describing group of users, related by shared funds and spending.

        Attributes:
            name (str): Name of user's group.
            icon (str, optional): Name of the file with group's avatar.
            owner (FK): ID owner of this group.
            members: Relation realization between users and groups.
            shared_funds: Relation realization between funds and groups.
            shared_spendings: Relation realization between spending and groups.


    """
    name = models.CharField(max_length=30)
    icon = models.CharField(max_length=30)
    owner = models.ForeignKey(UserProfile, on_delete=False)
    members = models.ManyToManyField(UserProfile,
                                     through='UsersInGroups',
                                     related_name="groups")
    shared_funds = models.ManyToManyField(FundCategories,
                                          through='SharedFunds',
                                          related_name="groups")
    shared_spendings = models.ManyToManyField(SpendingCategories,
                                              through='SharedSpendingCategories',
                                              related_name="groups")

    @staticmethod
    def group_filter_by_owner_id(user):
        """
        Args:
            user_id (int): index of owner,
        Returns:
            Group object if database contain group with user_id
        """
        return Group.objects.filter(owner=user)


    @staticmethod
    def get_group_by_id(group_id):
        """
        Args:
            group_id(int): The first parameter.
        Returns:
            Groups object if database contain with group_id , None otherwise.

        """
        try:
            group = Group.objects.get(pk=group_id)
            return group
        except Group.DoesNotExist:
            return None


class UsersInGroups(models.Model):
    """Members of groups.

        Attributes:
            group (FK): Group ID.
            user (FK): User ID.
            is_admin (bool):  "True" if user has right of administrator, "False" in other way.


    """
    group = models.ForeignKey(Group, on_delete=True)
    user = models.ForeignKey(UserProfile, on_delete=True)
    is_admin = models.BooleanField()

    @staticmethod
    def get_by_id(user_id):
        """
        Args:
            user_id(PK): The first parameter.
        Returns:
            UsersInGroups object if database contain user with user_id , None otherwise.

        """

        try:
            user = UsersInGroups.objects.get(pk=user_id)
            return user
        except UsersInGroups.DoesNotExist:
            return None


class SharedFunds(models.Model):
    """Common fund categories for groups.

        Attributes:
            group (FK): Group ID.
            fund (FK): Fund category ID.


    """
    group = models.ForeignKey(Group, on_delete=True)
    fund = models.ForeignKey(FundCategories, on_delete=True)


class SharedSpendingCategories(models.Model):
    """Common spending categories for groups.

        Attributes:
            group (FK): Group ID.
            spending_categories (FK): Spending category ID.


    """
    group = models.ForeignKey(Group, on_delete=True)
    spending_categories = models.ForeignKey(SpendingCategories, on_delete=True)
