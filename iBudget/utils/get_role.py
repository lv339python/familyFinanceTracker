"""
Provides functions to view roles
"""

from authentication.models import UserProfile
from group.models import Group, UsersInGroups


def is_user_sys_admin(user):
    """
    Checks if user is sys admin
    :param user(int):foreign key User ID
    :return:if user is sys_admin
    """
    return user.is_sys_admin


def groups_for_user(user):
    """
    Checks groups for user
    :param user(int):foreign key User ID
    :return:list group
    """

    group = Group.objects.filter(members=user)
    list_group = []
    for item in group:
        list_group.append(item.id)
    return list_group


def is_user_in_group(user, group_id):
    """
    Checks if user in group
    :param user(int):foreign key User ID
    :param group_id(PK):Group ID
    :return (boot): "True" if user in group, "False" in other way.
    """
    if group_id in groups_for_user(user):
        return True
    return False


def is_user_admin_group(user, group_id):
    """
    Checks if user in group is admin.
    :param user(int):foreign key User ID
    :param group_id(PK):Group ID
    :return(boot): "True" if user in group,is admin "False" in other way.
    """
    try:
        user_in_group = UsersInGroups.objects.get(user=user, group=Group.get_group_by_id(group_id))
        return user_in_group.is_admin
    except UsersInGroups.DoesNotExist:
        return False


def is_user_member_group(user, group_id):
    """
    Checks if user in group is admin.
    :param user(int):foreign key User ID
    :param group_id(PK):Group ID
    :return(boot): "True" if user a group member, "False" in other way.
    """
    try:
        user_in_group = UsersInGroups.objects.get(user=user, group=Group.get_group_by_id(group_id))
        return not user_in_group.is_admin
    except UsersInGroups.DoesNotExist:
        return False


def user_roles(user):
    """
    Checks user roles.
    :param user(int):foreign key User ID
    :return: dict data type
    """
    list_gr = groups_for_user(user)
    result = {}
    if list_gr:
        for item in list_gr:
            result[item] = 'admin' if is_user_admin_group(user=user, group_id=item) \
                else 'member'
    return result


def all_user_roles():
    """
    Checks all user roles.
    :return: dict data type
    """
    result = {}
    users = UserProfile.objects.all()
    for user in users:
        result[user.id] = user_roles(user)
    return result
