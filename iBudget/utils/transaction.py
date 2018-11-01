"""Save to DB with transaction"""
from django.db import transaction, IntegrityError

from fund.models import FundCategories, FinancialGoal
from group.models import SharedFunds, Group, UsersInGroups


def save_new_fund(name, icon, is_shared, owner, shared_group):
    """Function for safe save FundCategories and SharedFunds
    Args:
        name(str): name of category.
        icon(str): name of icon.
        is_shared(bool): if FundCategories is shared to some group True, else False.
        owner(UserProfile): transaction owner.
        shared_group(int): group to which the category is bound.
    Returns:
        True if success, False else
    """
    new_fund = FundCategories(
        name=name,
        icon=icon,
        is_shared=is_shared,
        owner=owner
    )
    try:
        with transaction.atomic():
            new_fund.save()
            if is_shared:
                group = Group.get_group_by_id(shared_group)
                shared_fund = SharedFunds(
                    group=group,
                    fund=new_fund)
                shared_fund.save()
    except IntegrityError:
        return False
    return True


def save_new_goal(value, # pylint: disable=too-many-arguments
                  start_date,
                  finish_date,
                  name,
                  icon,
                  is_shared,
                  owner,
                  shared_group):
    """Function for safe save FundCategories, Financialgoal and SharedFunds
    Args:
        name(str): name of category.
        icon(str): name of icon.
        is_shared(bool): if FundCategories is shared to some group True, else False.
        owner(UserProfile): transaction owner.
        value: value of your goal.
        start_date (date): The beginning of goal period
        finish_date (date): The end of goal period
        shared_group(int): group to which the category is bound.
    Returns:
        True if success, False else
    """
    fund = FundCategories(
        is_shared=is_shared,
        name=name,
        icon=icon,
        owner=owner)

    try:
        with transaction.atomic():
            fund.save()
            new_goal = FinancialGoal(
                value=value,
                start_date=start_date,
                finish_date=finish_date,
                fund=fund)
            new_goal.save()
            if is_shared:
                group = Group.get_group_by_id(shared_group)
                shared_fund = SharedFunds(
                    group=group,
                    fund=fund)
                shared_fund.save()
    except IntegrityError:
        return False
    return True


def save_new_group(name, icon, owner):
    """Function for safe save FundCategories and SharedFunds
    Args:
        name(str): name of group.
        icon(str): name of icon.
        owner(UserProfile): transaction owner.
    Returns:
        True if success, False else
    """
    new_group = Group(
        name=name,
        icon=icon,
        owner=owner
    )
    try:
        with transaction.atomic():
            new_group.save()
            new_users_in_group = UsersInGroups(
                group=new_group,
                user=owner,
                is_admin=True
            )
            new_users_in_group.save()
    except IntegrityError:
        return False
    return True
