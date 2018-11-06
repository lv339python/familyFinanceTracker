"""
Provides functions to view roles
"""

from authentication.models import UserProfile
from group.models import Group, UsersInGroups


def is_user_sys_admin(user):

    """
    Checks if user is sys admin
    :param user(int):foreign key User ID
    :return(bool): "True" if user is admin "False" in other way.
    """

    if user.is_sys_admin:
        return True
    return False


def users_email_for_group(group_id):
    """
    Checks user's email for group
    :param group_id:foreign key User ID
    :return:list list_users_email
    """
    group = UsersInGroups.objects.filter(group=group_id)
    list_users_email = []
    for item in group:
        list_users_email.append(item.user)
    return list_users_email


def groups_for_user(user):

    """
    Checks groups for user
    :param user(int):foreign key User ID
    :return:list groups_for_user
    """

    group = Group.objects.filter(members=user)
    list_group = []
    for item in group:
        list_group.append(item.id)
    return list_group


def is_user_in_group(group_id, user):

    """
    Checks if user in group
    :param user(int):foreign key User ID
    :param group_id(PK):Group ID
    :return (bool): "True" if user in group, "False" in other way.
    """

    try:
        UsersInGroups.objects.get(group=group_id, user=user)
        return True
    except UsersInGroups.DoesNotExist:
        return False


def is_user_admin_group(group_id, user):

    """
    Checks if user in group is admin.
    :param user(int):foreign key User ID
    :param group_id(PK):Group ID
    :return(bool): "True" if user in group,is admin "False" in other way.

    """

    try:
        user_in_group = UsersInGroups.objects.get(group=group_id, user=user)
        return user_in_group.is_admin
    except UsersInGroups.DoesNotExist:
        return False


def is_user_member_group(group_id, user):

    """
    Checks if user in group is admin.
    :param user(int):foreign key User ID
    :param group_id(PK):Group ID
    :return(bool): "True" if user a group member, "False" in other way.

    """

    try:
        user_in_group = UsersInGroups.objects.get(group=group_id, user=user)
        return not user_in_group.is_admin
    except UsersInGroups.DoesNotExist:
        return False


def user_teams_roles(user):

    """
    Checks user teams roles.
    :param user(int):foreign key User ID
    :return: dict data type
    """

    list_group = groups_for_user(user)
    result = {}
    for item in list_group:
        result[item] = 'admin' if is_user_admin_group(user=user, group_id=item) else 'member'
    return result


def user_all_roles():

    """
    Checks all user roles.
    :return: dict data type
    """

    result = {}
    users = UserProfile.objects.all()
    for user in users:
        result[user.id] = user_teams_roles(user)
    return result
