"""
This module provides functions for handling group view.
"""
import json

from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods

from authentication.models import UserProfile
from income_history.models import IncomeHistory
from spending_history.models import SpendingHistory
from utils.aws_helper import AwsService
from utils.get_role import groups_for_user, \
    is_user_admin_group, \
    is_user_in_group
from utils.transaction import save_new_group
from utils.validators import is_valid_data_create_new_group, \
    is_valid_data_add_user_to_group
from .models import Group, UsersInGroups


@require_http_methods(["GET"])
def get_by_group(request):
    """Handling request for creating of group list.
        Args:
            request (HttpRequest): request from server which ask some data.
        Returns:
            HttpResponse object.
    """

    user = request.user
    if user:
        user_groups = []
        for entry in Group.filter_groups_by_user_id(user):
            user_groups.append({'id': entry.id, 'name': entry.name})
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
            count = UsersInGroups.count_of_user_in_group(group.id)
            if group.owner == user:
                user_role = "Owner"
            else:
                if is_user_admin_group(item, user):
                    user_role = "Admin"
                else:
                    user_role = "Member"
            groups.append({'id': item, 'user_role': user_role, 'group_name': group.name, 'count': count})
        return JsonResponse(groups, status=200, safe=False)
    return JsonResponse({}, status=400)


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
    group = Group.get_group_by_id(data["group"])
    if is_user_in_group(group, user_add):
        return HttpResponse(status=409)
    if not user_add:
        return HttpResponse(status=406)
    if not group:
        return HttpResponse(status=406)
    if user:
        new_user = UsersInGroups(
            user=user_add,
            group=group,
            is_admin=is_admin
        )
        try:
            new_user.save()
            return HttpResponse(status=201)
        except(AttributeError, ValueError):
            return HttpResponse(status=400)
