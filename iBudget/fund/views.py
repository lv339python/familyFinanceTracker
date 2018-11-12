"""
This module provides functions for handling fund view.
"""

import json
from decimal import Decimal
from datetime import date, timedelta
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods

from group.models import Group, SharedFunds
from income_history.models import IncomeHistory
from spending_history.models import SpendingHistory
from utils.get_role import is_user_admin_group
from utils.transaction import save_new_fund, save_new_goal
from utils.validators import \
    input_fund_registration_validate, \
    date_range_validate, \
    is_valid_data_create_new_fund
from utils.aws_helper import AwsService
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
    icon_if_none = \
        'https://s3.amazonaws.com/family-finance-tracker-static/standard_fund/funds.png'
    if user:
        user_funds = []
        for entry in FundCategories.filter_by_user(user):
            if not FinancialGoal.has_goals(fund_id=entry.id):
                user_funds.append({'id': entry.id, 'name': entry.name, 'url':
                AwsService.get_image_url(entry.icon) if entry.icon else icon_if_none})
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
    icon_if_none = \
        'https://s3.amazonaws.com/family-finance-tracker-static/standard_fund/funds.png'
    if user:
        for group in Group.filter_groups_by_user_id(user):
            for shared_fund in SharedFunds.objects.filter(group=group.id):
                if not FinancialGoal.has_goals(fund_id=shared_fund.fund.id):
                    icon = FundCategories.objects.get(id=shared_fund.fund.id).icon
                    users_group.append({'id_fund': shared_fund.fund.id,
                                        'name_fund': shared_fund.fund.name,
                                        'id_group': group.id,
                                        'url': AwsService.get_image_url(icon) if icon else
                                        icon_if_none
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
    if not date_range_validate(data):
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

def create_initial_balance(user, begin_date, start_date, fund_id):
    """Creating fund balance.
            Args:
                user (UserProfile): user.
                begin_date (date): the beginning of statistic period for this user
                start_date (date): the beginning of statistic period
                fund_id (int): fund ID
            Returns:
                Balance value
    """
    return sum(IncomeHistory.filter_by_fund_id(fund_id).filter(
        date__range=[begin_date - timedelta(days=1),
                     start_date]).values_list('value', flat=True)) -\
           sum(SpendingHistory.filter_by_user_date(
               user,
               begin_date,
               start_date).filter(fund=fund_id).values_list('value', flat=True))

def create_balance(user, begin_date, start_date, finish_date, fund_id):
    """Creating fund balance.
            Args:
                user (UserProfile): user.
                begin_date (date): the beginning of statistic period for this user
                start_date (date): the beginning of statistic period
                finish_date (date): the end of statistic period
                fund_id (int): fund ID
            Returns:
                Balance value
    """

    return sum(IncomeHistory.filter_by_fund_id(fund_id).filter(
        date__range=[start_date - timedelta(days=1),
                     finish_date]).values_list('value', flat=True)) - \
           sum(SpendingHistory.filter_by_user_date(
               user,
               start_date,
               finish_date).filter(fund=fund_id).values_list('value', flat=True)) + \
           create_initial_balance(user, begin_date, start_date, fund_id)


@require_http_methods(["GET"])
def get_balance(request):
    """Handling request for creating spending history data.

        Args:
            request (HttpRequest): contains start date, final date and UTC information.
        Returns:
            JsonResponse object.
    """
    user = request.user
    current_date = date.today()
    start_date = date(current_date.year, current_date.month, 1)

    user_funds = []
    for item in FundCategories.filter_by_user(user):
        if not FinancialGoal.has_goals(fund_id=item.id):
            user_funds.append(item.id)

    for group in Group.filter_groups_by_user_id(user):
        for shared_fund in SharedFunds.objects.filter(group=group.id):
            if not FinancialGoal.has_goals(fund_id=shared_fund.fund.id):
                user_funds.append(shared_fund.fund.id)

    begin_date = min(
        min(SpendingHistory.objects.filter(owner=user).values_list(
            'date', flat=True)).date(),
        min(IncomeHistory.objects.filter(fund__in=user_funds).values_list(
            'date', flat=True)).date())
    response = []
    for item in user_funds:
        fund_initial = [create_initial_balance(user, begin_date, start_date, item)]
        fund_balance = [create_balance(user, begin_date, start_date, current_date, item)]
        dates = [str(current_date.month) + '/' + str(current_date.year)]
        while start_date > begin_date:
            finish_date = start_date - timedelta(days=1)
            start_date = date(finish_date.year, finish_date.month, 1)
            fund_initial.append(create_initial_balance(user, begin_date, start_date, item))
            fund_balance.append(create_balance(user, begin_date, start_date, finish_date, item))
            dates.append(str(finish_date.month) + '/' + str(finish_date.year))
        data = {'name': FundCategories.get_by_id(item).name,
                'initial': fund_initial,
                'balance': fund_balance}
        response.append(data)
        return JsonResponse(data, status=200, safe=False)
    return JsonResponse({}, status=400)
