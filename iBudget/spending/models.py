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


    """
    name = models.CharField(max_length=30)
    icon = models.CharField(max_length=30)
    owner = models.ForeignKey(UserProfile, on_delete=True)
    is_shared = models.BooleanField(default=False)

    def __str__(self):
        """
        :return: All the information about categories spending which is added.
        """
        return str(self.to_dict())[:]

    def __repr__(self):
        """
        :return: Basic information which includes categories spending.
        """
        return f"id:{self.id} name:{self.name}"

    def to_dict(self):
        """
        Convert information which added spendings to dictionary where
        key is description of added information and value is an information.
        """
        return {
            'id': self.id,
            'name': self.name,
            'icon': self.icon,
            'owner': self.owner,
            'is_shared':self.is_shared,
        }

    def update(self, name, owner, icon=None, is_shared=None):
        """
        Method which changes an information except owner as it is an id of an user.
        """

        if name:
            self.name = name
        if icon:
            self.icon = icon
        if owner:
            self.owner = owner
        if is_shared:
            self.is_shared = is_shared
        self.save()

    @classmethod
    def create(cls, name, icon=None, owner=None, is_shared=None):
        """
        Class method which creates categories of spending.
        """
        data = {}
        data["name"] = name
        data["icon"] = icon if icon else ""
        data["owner"] = owner if owner else ""
        data["is_shared"] = is_shared if is_shared else ""
        spending_categories = cls(**data)

        try:
            spending_categories.save()
            return spending_categories
        except (ValueError, AttributeError):
            pass

    @staticmethod
    def get_by_user_ind(user):
        """
        Args:
            user (FK): Owner of this category,
        Returns:
            List of spending categories for user if they exist, None otherwise.
        """
        try:
            return SpendingCategories.objects.filter(owner=user, is_shared=False)
        except SpendingCategories.DoesNotExist:
            return None

    @staticmethod
    def get_by_user_group(user):
        """
        Args:
            user (FK): Owner of this category,
        Returns:
            List of spending categories for user if they exist, None otherwise.
        """
        try:
            return SpendingCategories.objects.filter(owner=user, is_shared=True)
        except SpendingCategories.DoesNotExist:
            return None




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
        except SpendingCategories.DoesNotExist:
            return None



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
    def get_by_data(user, spending_category, start_date, finish_date):
        """
        Args:
            user (FK): Owner of this category.
            spending_category (FK): Spending category for individual purpose.
            start_date: The beginning of time period.
            finish_date: The end of time period.
        Returns:
            SpendingLimitationIndividual object if row with described data exists, None otherwise.


        """
        try:
            notice = SpendingLimitationIndividual.objects.filter(
                user=user,
                spending_category=spending_category,
                start_date=start_date,
                finish_date=finish_date)
            return notice
        except SpendingLimitationIndividual.DoesNotExist:
            return None




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
    finish_date = models.DateField()
    value = models.DecimalField(max_digits=17, decimal_places=2)
