"""
This module provides model of group and its relations.
"""
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
            user (int): index of owner,
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
            Groups object if database contain with group_id, None otherwise.

        """
        try:
            group = Group.objects.get(pk=group_id)
            return group
        except Group.DoesNotExist:
            return None

    @staticmethod
    def filter_groups_by_user_id(user_id):
        """
        Args:
            user_id(int): Current session user`s id.
        Returns:
            List of Groups objects .

        """
        users_groups = Group.objects.filter(members=user_id)
        return users_groups

    @staticmethod
    def filter_funds_by_group(group_object):
        """
        Args:
            group_object: users group object.
        Returns:
            List of fund objects for current group.

        """
        group_funds = []
        shared_funds = SharedFunds.objects.filter(group=group_object)
        for fund in shared_funds:
            for i in FundCategories.objects.filter(id=fund.id):
                group_funds.append({'id': i.id, 'name': i.name})
        return group_funds

    @staticmethod
    def filter_spendings_categories_by_group(group_object):
        """
        Args:
            group_object: users group object.
        Returns:
            List of spend objects for current group.

        """
        group_spendings = []
        shared_spendings = SharedSpendingCategories.objects.filter(group_id=group_object)
        for spend in shared_spendings:
            for i in SpendingCategories.objects.filter(id=spend.spending_categories_id):
                group_spendings.append({'id': i.id, 'name': i.name})
        return group_spendings


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
    def filter_by_group(group):
        """
        Implement searching of group members.

        Args:
            group (Group): group.
        Returns:
            List of group members if database contains them,
            None otherwise.

        """
        list_members = []
        for item in UsersInGroups.objects.filter(group=group):
            list_members.append(item.user)
        return list_members



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
    @staticmethod
    def filter_by_user(user):
        """
        Args:
            user (FK): user in group,
        Returns:
            UsersInGroup object if database contain group for user,
             None otherwise.

        """
        return UsersInGroups.objects.filter(user=user)

class SharedFunds(models.Model):
    """Common fund categories for groups.

        Attributes:
            group (FK): Group ID.
            fund (FK): Fund category ID.


    """
    group = models.ForeignKey(Group, on_delete=True)
    fund = models.ForeignKey(FundCategories, on_delete=True)

    @staticmethod
    def filter_by_group(group):
        """
        Implement searching of group fund categories.

        Args:
            group (Group): group for funds sharing.
        Returns:
            List of shared funds for group if database contains funds for group,
            None otherwise.

        """
        list_funds = []
        for item in SharedFunds.objects.filter(group=group):
            list_funds.append(item.fund)
        return list_funds


class SharedSpendingCategories(models.Model):
    """Common spending categories for groups.

        Attributes:
            group (FK): Group ID.
            spending_categories (FK): Spending category ID.


    """
    group = models.ForeignKey(Group, on_delete=True)
    spending_categories = models.ForeignKey(SpendingCategories, on_delete=True)

    @staticmethod
    def filter_by_group(group):
        """
        Implement searching of group spending categories.

        Args:
            group (Group): group for spending sharing.
        Returns:
            List of shared spending for group if database contains spending for group,
            None otherwise.

        """
        list_spendings = []
        for item in SharedSpendingCategories.objects.filter(group=group):
            list_spendings.append(item.spending_categories)
        return list_spendings
