"""
This module provides functions for handling group view.
"""
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from income_history.models import IncomeHistory
from spending_history.models import SpendingHistory
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
        for entry in Group.group_filter_by_owner_id(user):
            user_groups.append({'id': entry.id, 'name': entry.name, 'icon': entry.icon})
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
        group_balance[user_group.name] = {'Total income': 0, 'Total spending': 0}
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
