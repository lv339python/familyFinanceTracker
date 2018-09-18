from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class MyUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, icon, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            icon=icon,
        )

        user.set_password(password)
        user.save(using=self._db)

        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    icon = models.CharField(max_length=30)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'User'

class Group(models.Model):
    name = models.CharField(max_length=30)
    icon = models.CharField(max_length=30)
    owner = models.ForeignKey(MyUser, on_delete=True)
    class Meta:
        db_table = 'Group'

class UsersInGroups(models.Model):
    group = models.ForeignKey(Group, on_delete=True)
    user = models.ForeignKey(MyUser, on_delete=True)
    is_admin = models.BooleanField()
    class Meta:
        db_table = 'Users in groups'

class Funds(models.Model):
    name = models.CharField(max_length=30)
    icon = models.CharField(max_length=30)
    is_shared = models.BooleanField()
    user = models.ForeignKey(MyUser, on_delete=True)
    class Meta:
        db_table = 'Available funds'


class IncomeCategories(models.Model):
    name = models.CharField(max_length=30)
    user = models.ForeignKey(MyUser, on_delete=True)
    date = models.DateField(auto_now=True, auto_now_add=False)
    sum = models.DecimalField(max_digits=17, decimal_places=2)
    icon = models.CharField(max_length=30)
    class Meta:
        db_table = 'Income categories'

class SpendingCategories(models.Model):
    name = models.CharField(max_length=30)
    user = models.ForeignKey(MyUser, on_delete=True)
    icon = models.CharField(max_length=30)
    is_shared = models.BooleanField()
    class Meta:
        db_table = 'Spending categories'

class SharedFunds(models.Model):
    funds = models.ForeignKey(Funds, on_delete=True)
    group = models.ForeignKey(Group, on_delete=True)
    class Meta:
        db_table = 'Shared funds'


class SharedSpendingCategories(models.Model):
    group = models.ForeignKey(Group, on_delete=True)
    spending_categories = models.ForeignKey(SpendingCategories, on_delete=True)
    class Meta:
        db_table = 'Shared spending categories'

class IncomeHistory(models.Model):
    income = models.ForeignKey(IncomeCategories, on_delete=True)
    funds = models.ForeignKey(Funds, on_delete=True)
    date = models.DateTimeField(auto_now=True, auto_now_add=False)
    sum = models.DecimalField(max_digits=17, decimal_places=2)
    comment = models.TextField()
    class Meta:
        db_table = 'Income history'

class SpendingHistory(models.Model):
    funds = models.ForeignKey(Funds, on_delete=True)
    spending_categories = models.ForeignKey(SpendingCategories, on_delete=True)
    sum = models.DecimalField(max_digits=17, decimal_places=2)
    date = models.DateTimeField(auto_now=True, auto_now_add=False)
    owner = models.ForeignKey(MyUser, on_delete=True)
    comment = models.TextField()
    class Meta:
        db_table = 'Spending history'

