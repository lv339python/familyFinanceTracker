"""
    Function that provides for receiving roles
"""
from authentication.models import UserProfile
from group.models import UsersInGroups


def get_user_roles(user_id):
    """
    Current function checks and returns user roles in dict data type

    :param user_id: int
    :return: role_dict
    """
    role_dict = {
        'sys_admin': False,
        'admin': False,
        'member': False,
        'user': False

    }

    user = UserProfile.get_by_id(user_id)
    if user.is_sys_admin:
        role_dict['sys_admin'] = True
    if user:
        role_dict['user'] = True
    user = UsersInGroups.get_by_id(user_id)
    if user and user.is_admin:
        role_dict['admin'] = True
    if user:
        role_dict['member'] = True
    return role_dict
