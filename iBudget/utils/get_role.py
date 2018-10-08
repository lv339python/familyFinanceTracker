"""
    Function that provides for receiving roles
"""
from authentication.models import UserProfile
from group.models import UsersInGroups


class UserRoles:  #pylint: disable=too-few-public-methods
    """
    User's roles.
    """
    @staticmethod
    def get_role():
        """
        Current function checks and returns user roles in dict data type
        :return: role_dict
        """
        role_dict = {
            'sys_admin': [],
            'admin': [],
            'member': [],
            'user': []
        }

        user_list = UserProfile.objects.all()
        users = UsersInGroups.objects.all()

        for user in user_list:
            if user.is_sys_admin:
                role_dict['sys_admin'].append(user.first_name)
            if user:
                role_dict['user'].append(user.first_name)
        for user in users:
            if user.is_admin:
                role_dict['admin'].append(user.id)
            if user.user:
                role_dict['member'].append(user.id)
        admins_names = []
        for user_id in role_dict['admin']:
            admins_names.append(UserProfile.get_by_id(user_id).first_name)
        role_dict['admin'] = admins_names

        members_names = []
        for user_id in role_dict['member']:
            members_names.append(UserProfile.get_by_id(user_id).first_name)
        role_dict['member'] = members_names
        return role_dict
