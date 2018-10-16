"""
This module provides functions for handling group view.
"""
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Group



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
            user_groups.append({'id': entry.id, 'name': entry.name})
        return JsonResponse(user_groups, status=200, safe=False)
    return JsonResponse({}, status=400
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
        income_values, spend_values = [], []
        for fund in Group.filter_funds_by_group(user_group):
            income_values.extend(IncomeHistory.objects.filter(fund=fund.id))
        for i in income_values:
            group_balance[user_group.name]['Total income'] += i.value
        for spend in Group.filter_spendings_categories_by_group(user_group):
            spend_values.extend(SpendingHistory.objects.filter(spending_categories_id=spend.id))
        for i in spend_values:
            group_balance[user_group.name]['Total spending'] += i.value
        group_balance[user_group.name]["Current balance"] = \
            group_balance[user_group.name]['Total income'] - \
            group_balance[user_group.name]['Total spending']
    return JsonResponse(group_balance)
