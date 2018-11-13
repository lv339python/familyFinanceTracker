"""
This module provides functions for handling group view.
"""
import json

from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from fund.models import FundCategories
from group.models import SpendingCategories, SharedSpendingCategories, SharedFunds
from authentication.models import UserProfile
from income_history.models import IncomeHistory
from spending_history.models import SpendingHistory
from utils.aws_helper import AwsService
from utils.get_role import groups_for_user, \
    is_user_admin_group, \
    is_user_in_group, \
    users_email_for_group
from utils.transaction import save_new_group
from utils.validators import is_valid_data_create_new_group, \
    is_valid_data_add_user_to_group, \
    is_valid_data_shared_spending_to_group, \
    is_valid_data_shared_fund_to_group
from .models import Group, UsersInGroups

# CONSTANTS FOR ICONS
AWS_S3_URL = 'https://s3.amazonaws.com/family-finance-tracker-static/'
STANDARD_GROUPS_FOLDER = 'standard_group/'
ICON_FILE_NAME = 'group.png'


@require_http_methods(["GET"])
def get_by_group(request):
    """Handling request for creating of group list.
        Args:
            request (HttpRequest): request from server which ask some data.
        Returns:
            HttpResponse object.
    """

    user = request.user
    icon_if_none = AWS_S3_URL + STANDARD_GROUPS_FOLDER + ICON_FILE_NAME
    if user:
        user_groups = []
        for entry in Group.filter_groups_by_user_id(user):
            url = AwsService.get_image_url(entry.icon) if entry.icon else icon_if_none
            user_groups.append({'id': entry.id, 'name': entry.name,
                                'url': url})
        return JsonResponse(user_groups, status=200, safe=False)
    return JsonResponse({}, status=400)


@require_http_methods(["GET"])
def show_users_group(request):
    """Handling request for creating of user's groups list.
    Args:
        request (HttpRequest): request from server which ask list of groups for user.
    Returns:
        HttpResponse object.
    """
    user = request.user
    if user:
        groups = []
        for item in UsersInGroups.filter_by_user(user):
            groups.append({'name': item.group.name, 'id': item.group.id})
        return JsonResponse(groups, status=200, safe=False)
    return JsonResponse({}, status=400)


@require_http_methods(["GET"])
def show_users_group_data(request):
    """Handling request for creating of user's groups list.
    Args:
        request (HttpRequest): request from server which ask list of groups data for user.
    Returns:
        HttpResponse object.
    """
    user = request.user
    if user:
        groups = []
        user_role = None
        for item in groups_for_user(user):
            group = Group.get_group_by_id(item)
            count = users_email_for_group(group.id)
            if group.owner == user:
                user_role = "Owner"
            else:
                if is_user_admin_group(item, user):
                    user_role = "Admin"
                else:
                    user_role = "Member"
            groups.append({'id': item,
                           'user_role': user_role,
                           'group_name': group.name,
                           'count': len(count)})
        return JsonResponse(groups, status=200, safe=False)
    return JsonResponse({}, status=400)


def show_users_in_group(request):
    """Handling request for creating of group's users list.
    Args:
        request (HttpRequest): request from server which ask list of users for group.
    Returns:
        HttpResponse object.
    """
    users_in_group = []
    user = request.user
    user_role = None
    if user:
        for item in groups_for_user(user):
            group = Group.get_group_by_id(item)
            for user in users_email_for_group(group.id):
                if group.owner == user:
                    user_role = "Owner"
                else:
                    if is_user_admin_group(item, user):
                        user_role = "Admin"
                    else:
                        user_role = "Member"
                users_in_group.append({'email': user.email,
                                       'user_role': user_role,
                                       'group_id': group.id})
        return JsonResponse(users_in_group, status=200, safe=False)
    return HttpResponse(status=400)


def groups_balance(request):
    """
    Retrieving group`s budget information
    Args:
        request: request from the website
    Returns:
        Group-balance is dictionary which contains Total spendings,
        Total funds and Balance for every user`s group.
    """
    user_id = request.user.id
    group_balance = {}
    users_groups = Group.filter_groups_by_user_id(user_id)
    for user_group in users_groups:
        group_balance[user_group.name] = {'Total income': 0,
                                          'Total spending': 0,
                                          'Group icon': AwsService.get_image_url(user_group.icon),
                                          'Group_id': user_group.id}
        income_values = filter_income_history_by_fund(user_group)
        for i in income_values:
            group_balance[user_group.name]['Total income'] += i['value']
        spend_values = filter_spending_history_by_spend_category(user_group)
        for i in spend_values:
            group_balance[user_group.name]['Total spending'] += i['value']
        group_balance[user_group.name]["Current balance"] = \
            group_balance[user_group.name]['Total income'] - \
            group_balance[user_group.name]['Total spending']
    return JsonResponse(group_balance)


def filter_income_history_by_fund(user_group):
    """
    Retrieving income history information by users group for shared funds
    Args:
        user_group: specific users group
    Returns:
        income_values: list of dictionaries consisting id,value and fund-name
    """
    income_values = []
    for fund in Group.filter_funds_by_group(user_group):
        for i in IncomeHistory.objects.filter(fund=fund['id']):
            income_values.append({'id': i.id, 'value': i.value,
                                  'fund_name': i.fund})
    return income_values


def filter_spending_history_by_spend_category(user_group):
    """
    Retrieving spending history information by users group for shared spendings
    Args:
        user_group: specific users group
    Returns:
        income_values: list of dictionaries consisting id,value and spend-name
    """
    spend_values = []
    for spend in Group.filter_spendings_categories_by_group(user_group):
        for i in SpendingHistory.objects.filter(spending_categories_id=spend['id']):
            spend_values.append({'id': i.id, 'value': i.value, 'spend_name': i.spending_categories})
    return spend_values


@require_http_methods(["POST"])
def create_new_group(request):
    """Handling request for creating of new user's group.
    Args:
        request (HttpRequest): request from server which contain
            name, icon
    Returns:
        HttpResponse object.
    """
    data = json.loads(request.body)
    user = request.user
    if not is_valid_data_create_new_group(data):
        return HttpResponse(status=400)
    if save_new_group(name=data["name"], icon=data["icon"], owner=user):
        return HttpResponse(status=201)
    return HttpResponse(status=406)


@require_http_methods(["POST"])
def add_new_users_to_group(request):
    """Handling request for adding new user to group.
   Args:
       request (HttpRequest): request from server which contain
           email, group and is_admin(True or False)
   Returns:
       HttpResponse object.
   """
    data = json.loads(request.body)
    user = request.user
    if not is_valid_data_add_user_to_group(data):
        return HttpResponse(status=400)
    user_add = UserProfile.get_by_email(data["users_email"])
    is_admin = data["is_admin"]
    group = Group.get_group_by_id(data["group_id"])
    if not is_user_admin_group(group.id, user):
        return HttpResponse(status=403)
    if is_user_in_group(group, user_add):
        return HttpResponse(status=409)
    if not user_add and not group:
        return HttpResponse(status=406)
    if user:
        new_user = UsersInGroups(
            user=user_add,
            group=group,
            is_admin=is_admin
        )
        try:
            new_user.save()
        except(AttributeError, ValueError):
            return HttpResponse(status=400)
    return HttpResponse(status=201)


@require_http_methods(["POST"])
def add_shared_spending_to_group(request):
    """Handling request for adding new shared SpendingCategories to group.
    Args:
        request (HttpRequest): request from server which contain
        shared_spending and group_id
    Returns:
        HttpResponse object.
    """
    user = request.user
    data = json.loads(request.body)
    shared_category = data["shared_spending"]
    group_id = data["group_id"]
    spending = SpendingCategories.get_by_id(shared_category)
    group = Group.get_group_by_id(group_id)
    if not is_valid_data_shared_spending_to_group(data):
        return HttpResponse(status=400)
    if not is_user_admin_group(group_id, user) and not spending.owner == user:
        return HttpResponse(status=409)
    if not spending and not group:
        return HttpResponse(status=406)
    if SharedSpendingCategories.get_by_spending_id(spending):
        return HttpResponse(status=409)
    new_shared_category = SharedSpendingCategories(
        group=group,
        spending_categories=spending
    )
    spending.is_shared = True
    try:
        new_shared_category.save()
        spending.save()
    except(AttributeError, ValueError):
        return HttpResponse(status=400)
    return HttpResponse(status=201)


@require_http_methods(["POST"])
def add_shared_fund_to_group(request):
    """Handling request for adding new shared SpendingCategories to group.
    Args:
        request (HttpRequest): request from server which contain
        shared_spending and group_id
    Returns:
        HttpResponse object.
    """
    user = request.user
    data = json.loads(request.body)
    shared_category = data["shared_fund"]
    group_id = data["group_id"]
    fund = FundCategories.get_by_id(shared_category)
    group = Group.get_group_by_id(group_id)
    if not is_valid_data_shared_fund_to_group(data):
        return HttpResponse(status=400)
    if not is_user_admin_group(group_id, user) and not fund.owner == user:
        return HttpResponse(status=409)
    if not fund and not group:
        return HttpResponse(status=406)
    if SharedFunds.get_by_fund(fund):
        return HttpResponse(status=409)
    new_shared_fund = SharedFunds(
        group=group,
        fund=fund
    )
    fund.is_shared = True
    try:
        new_shared_fund.save()
        fund.save()
    except(AttributeError, ValueError):
        return HttpResponse(status=400)
    return HttpResponse(status=201)


@require_http_methods(["POST"])
def change_users_role_in_group(request):
    """Handling request for updating user's role in group.
    Args:
        request (HttpRequest): request from server which contain
        email, is_admin and group_id
    Returns:
        HttpResponse object.
    """
    data = json.loads(request.body)
    print(data)
    user_email = data["user_email"]
    group_id = data["group_id"]
    is_admin = data["is_admin"]
    user_to_change = UserProfile.get_by_email(user_email)
    is_admin = True if is_admin == 'Admin' else False
    user = request.user
    if user:
        if not is_user_admin_group(group_id, user):
            return HttpResponse(status=409)
        if not is_user_in_group(group_id, user_to_change.id):
            return HttpResponse(status=406)
        group = UsersInGroups.get_by_id(user_to_change.id)
        group.is_admin = is_admin
        try:
            group.save()
        except(ValueError, AttributeError):
            return HttpResponse(status=400)
    return HttpResponse(status=200)


# <button
#                                         v-if="user.user_role!='Owner'"
#                                         type="button"
#                                         class="btn btn-primary"
#                                         @click="changeRole(user.email)"
#                                         >
#                                             {{ user.user_role }}
#                                     </button>
