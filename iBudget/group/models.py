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

    def to_dict(self):
      """
      Convert information team object to dictionary where
      key is description of added information and value is an information.
      """
      members = [user.id for user in self.members.all()] if self.members else []
      shared_funds = [funds.id for funds in self.shared_funds.all()] if self.shared_funds else[]
      shared_spendings=[spendings.id for spendings in self.shared_spendings.all()] if self.shared_spendings else[]
      return {
        'id': self.id,
        'name': self.name,
        'icon': self.icon,
        'owner': self.owner,
        'members_id': members,
        'shared_funds': shared_funds,
        'shared_spendings': shared_spendings,
      }

    @classmethod
    def create(cls, owner, name, icon=None):
      """
      Class method with create group
      """
      data = {}
      data["owner"] = owner if owner else ""
      data["name"] = name if name else ""
      data["icon"] = icon if icon else ""
      group = cls(**data)
      try:
        group.save()
        return group
      except (ValueError, AttributeError):
        pass

    @staticmethod
    def get_by_id(group_id):

      """
      returns object of Group by id
      """
      try:
        group = Group.objects.get(id=group_id)
        return group
      except Group.DoesNotExist:
        return None

    @staticmethod
    def get_groups_by_owner(owner_id):
      try:
        group=Group.objects.get(owner=owner_id)
        return group
      except Group.DoesNotExist:
        return None


    @staticmethod
    def delete_by_id(group_id):
      """
      :param user_id: an id of a user to be deleted
      :type user_id: int
      :return: True if object existed in the db and was removed or False if it didn't exist
      """

      try:
        group = Group.objects.get(id=group_id)
        group.delete()
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

    @classmethod
    def create(cls, is_admin=None):
      """
      Class method with create group
      """
      data = {}
      data["is_admin"] = is_admin if is_admin else ""
      admin = cls(**data)
      try:
        admin.save()
        return admin
      except (ValueError, AttributeError):
        pass

    @staticmethod
    def get_user_id(user_in_groups_id):
      try:
        return UsersInGroups.objects.get(user=user_in_groups_id)
      except Group.DoesNotExist:
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




    @staticmethod
    def get_spend_by_group(group):

      """
            returns object of Group by id
      """
      try:
        return SharedSpendingCategories.objects.get(group=group)
      except SharedSpendingCategories.DoesNotExist:
        return None

    @staticmethod
    def get_spendinng_category(spending_categories):

      """
            returns object of Group by id
      """
      try:
        return SharedSpendingCategories.objects.get(spending_categories=spending_categories)
      except SharedSpendingCategories.DoesNotExist:
        return None


