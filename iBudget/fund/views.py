"""
This module provides functions for handling fund view.
"""

import json
from decimal import Decimal

from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods

from group.models import Group, SharedFunds
from income_history.models import IncomeHistory
from utils.get_role import is_user_admin_group
from utils.transaction import save_new_fund, save_new_goal
from utils.validators import \
    input_fund_registration_validate, \
    date_range_validate, \
    is_valid_data_create_new_fund
from .models import FundCategories, FinancialGoal


@require_http_methods(["GET"])
def show_fund(request):
    """Handling request for creating of spending categories list.

        Args:
            request (HttpRequest): request from server which ask some data.
        Returns:
            HttpResponse object.
    """
    user = request.user
    if user:
        user_funds = []
        for entry in FundCategories.filter_by_user(user):
            user_funds.append({'id': entry.id, 'name': entry.name})
        return JsonResponse(user_funds, status=200, safe=False)
    return JsonResponse({}, status=400)


@require_http_methods(["GET"])
def show_fund_by_group(request):
    """Handling request for creating of spending categories list in group.
        Args:
            request (HttpRequest): Limitation data.
        Returns:
            HttpResponse object.
    """

    user = request.user
    users_group = []
    if user:
        for group in Group.filter_groups_by_user_id(user):
            for shared_fund in SharedFunds.objects.filter(group=group.id):
                users_group.append({'id_fund': shared_fund.fund.id,
                                    'name_fund': shared_fund.fund.name,
                                    'id_group': group.id
                                    })
        return JsonResponse(users_group, status=200, safe=False)
    return JsonResponse({}, status=400)


@require_http_methods(["GET"])
def show_goal_data(request):
    """Handling request for creating of goal data list.

       Args:
           request (HttpRequest): Goal data.
       Returns:
           JsonResponse object.
   """

    user = request.user
    if user:
        user_goal_statistic = []
        for entry in list_goal_user(user):
            fund_category = FundCategories.get_by_id(entry)
            list_transactions = []
            list_date_transactions = []
            for item in IncomeHistory.objects.filter(fund=entry,
                                                     date__range=[fund_category.goal.start_date,
                                                                  fund_category.goal.finish_date]):
                list_transactions.append(float(item.value))
                list_date_transactions.append(item.date)
            user_goal_statistic.append({"id": entry,
                                        "name": fund_category.name,
                                        "value": fund_category.goal.value,
                                        "start_date": fund_category.goal.start_date,
                                        "finish_date": fund_category.goal.finish_date,
                                        "transaction": list_transactions,
                                        "date_transaction": list_date_transactions})
        return JsonResponse(user_goal_statistic, status=200, safe=False)
    return JsonResponse({}, status=400)


def list_goal_user(user):
    """the functions finds all the user's goals associated with particular user and
    returns them

           Args:
               user (UserProfile): owner of this goal
            Return:
                Goals list

       """
    list_fund = []
    for entry in FundCategories.filter_by_user(user):
        list_fund.append(entry.id)
    for entry in FundCategories.filter_by_user(user, True):
        list_fund.append(entry.id)
    list_goal = []

    for entry in list_fund:
        financial_goal = FinancialGoal.objects.filter(fund=entry)
        if financial_goal:
            list_goal.append(entry)
    return list_goal


@require_http_methods(["GET"])
def users_shared_fund(request):
    """Handling request for creating of fund list in group.
        Args:
            request (HttpRequest): Limitation data.
        Returns:
            HttpResponse object.
    """

    user = request.user
    users_fund = []
    if user:
        for group in Group.group_filter_by_owner_id(user):
            for shared_fund in SharedFunds.objects.filter(group=group.id):
                users_fund.append({'id_fund': shared_fund.fund.id,
                                   'name_fund': shared_fund.fund.name,
                                   'id_group': group.id
                                   })
        return JsonResponse(users_fund, status=200, safe=False)
    return JsonResponse({}, status=400)


@require_http_methods(["POST"])
def register_financial_goal(request):
    """Handling request for creating of fund list.
        Args:
            request (HttpRequest): request from server which contain
            fund, value, start_date, finish_date
        Returns:
            HttpResponse status.
    """
    data = json.loads(request.body)
    if not input_fund_registration_validate(data):
        return HttpResponse(status=400)

    user = request.user
    fund = FundCategories.get_by_id(int(data["fund"]))
    if not fund:
        return HttpResponse(status=400)
    if not fund.owner == user:
        return HttpResponse(status=403)
    value = Decimal(data["value"])
    if not date_range_validate(data):
        return HttpResponse(status=400)

    financial_goal_group = FinancialGoal(value=value,
                                         start_date=data["start_date"],
                                         finish_date=data["finish_date"],
                                         fund=fund
                                         )
    try:
        financial_goal_group.save()
    except(ValueError, AttributeError):
        return HttpResponse(status=406)
    return HttpResponse(status=201)


@require_http_methods(["POST"])
def create_new_fund(request):
    """Handling request for creating of new fund category.
    Args:
        request (HttpRequest): request from server which contain
            shred_group, name, icon
    Returns:
        HttpResponse object.
    """
    data = json.loads(request.body)
    if not is_valid_data_create_new_fund(data):
        return HttpResponse(status=400)
    user = request.user
    shared_group = data["shared_group"]
    is_shared = False
    if shared_group:
        is_shared = True
        group = Group.get_group_by_id(shared_group)
        if not group:
            return HttpResponse(status=400)
        if not is_user_admin_group(group.id, user):
            return HttpResponse(status=406)
    if save_new_fund(name=data["name"],
                     icon=data["icon"],
                     is_shared=is_shared,
                     owner=user,
                     shared_group=shared_group):
        return HttpResponse(status=201)
    return HttpResponse(status=406)


@require_http_methods(["POST"])
def create_new_goal(request):
    """Handling request for creating of new goal category.
    Args:
        request (HttpRequest): request from server which contain
            value, start_date, finish_date, shred_group, name, icon
    Returns:
        HttpResponse object.
    """
    data = json.loads(request.body)
    if not input_fund_registration_validate(data):
        return HttpResponse(status=400)
    if not is_valid_data_create_new_fund(data):
        return HttpResponse(status=400)
    user = request.user
    shared_group = data["shared_group"]
    is_shared = False
    if shared_group:
        is_shared = True
        group = Group.get_group_by_id(shared_group)
        if not group:
            return HttpResponse(status=400)
        if not is_user_admin_group(group.id, user):
            return HttpResponse(status=406)
    if save_new_goal(
            value=Decimal(data["value"]),
            start_date=data["start_date"],
            finish_date=data["finish_date"],
            name=data["name"],
            icon=data["icon"],
            is_shared=is_shared,
            owner=user,
            shared_group=shared_group):
        return HttpResponse(status=201)
    return HttpResponse(status=409)
