from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class UserProfile(AbstractBaseUser):
    """A user's profile with the required fields "email", "password" and the user's image (optional).
    Parameters
    ----------
    email : 'string'
        User's email.
    icon : 'string'
       File's name.

    """
    # email = models.EmailField(max_length=50, unique=True)


    icon = models.CharField(max_length=30)

    objects = BaseUserManager()
    USERNAME_FIELD = 'email'


class IncomeCategories(models.Model):
    name = models.CharField(max_length=30)
    owner = models.ForeignKey(UserProfile, on_delete=True)
    date = models.DateField()
    value = models.DecimalField(max_digits=17, decimal_places=2)
    icon = models.CharField(max_length=30)


class FundsCategories(models.Model):
    name = models.CharField(max_length=30)
    icon = models.CharField(max_length=30)
    is_shared = models.BooleanField(default=False)
    owner = models.ForeignKey(UserProfile, on_delete=True)


class SpendingCategories(models.Model):
    name = models.CharField(max_length=30)
    owner = models.ForeignKey(UserProfile, on_delete=True)
    icon = models.CharField(max_length=30)
    is_shared = models.BooleanField(default=False)


class Group(models.Model):
    name = models.CharField(max_length=30)
    icon = models.CharField(max_length=30)
    owner = models.ForeignKey(UserProfile, on_delete=False)
    members = models.ManyToManyField(UserProfile,
                                     through='UsersInGroups',
                                     related_name="groups")
    shared_funds = models.ManyToManyField(FundsCategories,
                                          through='SharedFunds',
                                          related_name="groups")
    shared_spendings = models.ManyToManyField(SpendingCategories,
                                              through='SharedSpendingCategories',
                                              related_name="groups")


class IncomeHistory(models.Model):
    income = models.ForeignKey(IncomeCategories, on_delete=True, related_name="income_history")
    fund = models.ForeignKey(FundsCategories, on_delete=True, related_name="income_history")
    date = models.DateTimeField()
    value = models.DecimalField(max_digits=17, decimal_places=2)
    comment = models.TextField(null=True, default="")


class SpendingHistory(models.Model):
    fund = models.ForeignKey(FundsCategories, on_delete=True, related_name="spending_history")
    spending_categories = models.ForeignKey(SpendingCategories, on_delete=True, related_name="spending_history")
    value = models.DecimalField(max_digits=17, decimal_places=2)
    date = models.DateTimeField()
    owner = models.ForeignKey(UserProfile, on_delete=True)
    comment = models.TextField(null=True, default="")


class UsersInGroups(models.Model):
    group = models.ForeignKey(Group, on_delete=True)
    user = models.ForeignKey(UserProfile, on_delete=True)
    is_admin = models.BooleanField()


class SharedFunds(models.Model):
    group = models.ForeignKey(Group, on_delete=True)
    fund = models.ForeignKey(FundsCategories, on_delete=True)


class SharedSpendingCategories(models.Model):
    group = models.ForeignKey(Group, on_delete=True)
    spending_categories = models.ForeignKey(SpendingCategories, on_delete=True)
