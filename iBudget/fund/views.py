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
from utils.aws_helper import AwsService
from utils.get_role import is_user_admin_group
from utils.transaction import save_new_goal
from utils.universal_category_methods import total_value_for_category
from utils.validators import \
    input_fund_registration_validate, \
    date_range_validate, \
    is_valid_data_create_new_fund, \
    total_category_validation
from .models import FundCategories, FinancialGoal

# CONSTANTS FOR ICONS
AWS_S3_URL = 'https://s3.amazonaws.com/family-finance-tracker-static/'
STANDARD_FUNDS_FOLDER = 'standard_fund/'
ICON_FILE_NAME = 'funds.png'


@require_http_methods(["GET"])
def show_fund(request):
    """Handling request for creating of spending categories list.

        Args:
            request (HttpRequest): request from server which ask some data.
        Returns:
            HttpResponse object.
    """
    user = request.user
    icon_if_none = AWS_S3_URL + STANDARD_FUNDS_FOLDER + ICON_FILE_NAME
    if user:
        user_funds = []
        for entry in FundCategories.filter_by_user(user):
            url = AwsService.get_image_url(entry.icon) if entry.icon else icon_if_none
            if not FinancialGoal.has_goals(fund_id=entry.id):
                user_funds.append({'id': entry.id, 'name': entry.name,
                                   'url': url})
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
    icon_if_none = AWS_S3_URL + STANDARD_FUNDS_FOLDER + ICON_FILE_NAME
    if user:
        for group in Group.filter_groups_by_user_id(user):
            for shared_fund in SharedFunds.objects.filter(group=group.id):
                if not FinancialGoal.has_goals(fund_id=shared_fund.fund.id) \
                    and shared_fund.fund.is_active:
                    icon = FundCategories.objects.get(id=shared_fund.fund.id).icon
                    url = AwsService.get_image_url(icon) if icon else icon_if_none
                    users_group.append({'id_fund': shared_fund.fund.id,
                                        'name_fund': shared_fund.fund.name,
                                        'id_group': group.id,
                                        'url': url
                                        })
        return JsonResponse(users_group, status=200, safe=False)
    return JsonResponse({}, status=400)


@require_http_methods(["GET"])
def show_goal(request):
    """Handling request for creating of delete goals.

        Args:
            request (HttpRequest): request from server which ask some data.
        Returns:
            HttpResponse object.
    """
    user = request.user
    if user:
        user_funds = []
        for entry in FundCategories.filter_by_user(user):
            if FinancialGoal.has_goals(fund_id=entry.id):
                user_funds.append({'id': entry.id, 'name': entry.name})
        return JsonResponse(user_funds, status=200, safe=False)
    return JsonResponse({}, status=400)


@require_http_methods(["GET"])
def show_goal_by_group(request):
    """Handling request delete shared goal.
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
                if FinancialGoal.has_goals(fund_id=shared_fund.fund.id) \
                    and shared_fund.fund.is_active:
                    users_group.append({'id_fund': shared_fund.fund.id,
                                        'name_fund': shared_fund.fund.name,
                                        'id_group': group.id,
                                        'group_name': group.name
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
        request (HttpRequest): request from server which contain name and icon
    Returns:
        HttpResponse object.
    """
    data = json.loads(request.body)
    if not is_valid_data_create_new_fund(data):
        return HttpResponse(status=400)
    user = request.user
    new_fund = FundCategories(
        name=data["name"],
        icon=data["icon"],
        is_shared=False,
        owner=user
    )
    try:
        new_fund.save()
    except(ValueError, AttributeError):
        return HttpResponse(status=406)
    return HttpResponse(status=201)


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
                     start_date]).values_list('value', flat=True)) - \
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


def history_begin_date(user, user_funds):
    """Search the earliest date in user's history.
            Args:
                user (UserProfile): user.
                user_funds (list): list of user's fund ID
            Returns:
                The earliest history date if user has spending or fund history,
                current date otherwise.
    """
    current_date = date.today()
    list_date_spending = SpendingHistory.objects.filter(owner=user).values_list(
        'date', flat=True)
    list_date_fund = IncomeHistory.objects.filter(fund__in=user_funds).values_list(
        'date', flat=True)
    begin_date = min(list_date_spending).date() if list_date_spending else current_date
    begin_date = min(begin_date, min(list_date_fund).date()) if list_date_fund else begin_date
    return begin_date


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
    if user:
        user_funds = []
        for item in FundCategories.filter_by_user(user):
            if not FinancialGoal.has_goals(fund_id=item.id):
                user_funds.append(item.id)

        for group in Group.filter_groups_by_user_id(user):
            for item in SharedFunds.objects.filter(group=group.id):
                if not FinancialGoal.has_goals(fund_id=item.fund.id) \
                    and item.fund.is_active:
                    user_funds.append(item.fund.id)
        begin_date = history_begin_date(user, user_funds)
        name = []
        initial = []
        balance = []
        dates = [str(current_date.month) + '/' + str(current_date.year)]
        while start_date > begin_date:
            finish_date = start_date - timedelta(days=1)
            start_date = date(finish_date.year, finish_date.month, 1)
            dates.append(str(finish_date.month) + '/' + str(finish_date.year))

        for item in user_funds:
            fund_initial = [create_initial_balance(user, begin_date, start_date, item)]
            fund_balance = [create_balance(user, begin_date, start_date, current_date, item)]
            current_date = date.today()
            start_date = date(current_date.year, current_date.month, 1)
            while start_date > begin_date:
                finish_date = start_date - timedelta(days=1)
                start_date = date(finish_date.year, finish_date.month, 1)
                fund_initial.append(create_initial_balance(user, begin_date, start_date, item))
                fund_balance.append(create_balance(user, begin_date, start_date, finish_date, item))
            name.append(FundCategories.get_by_id(item).name)
            initial.append(fund_initial)
            balance.append(fund_balance)
        return JsonResponse({'fund': name,
                             'initial': initial,
                             'balance': balance,
                             'dates': dates}, status=200, safe=False)
    return JsonResponse({}, status=400)


@require_http_methods(["DELETE"])
def delete_fund_goal_category(request, fund_id):
    """Handling request for delete fund category.
        Args:
            request (HttpRequest): Data for delete fund.
            fund_id: Fund category Id
        Returns:
            HttpResponse object.
    """

    user = request.user
    if user:
        fund = FundCategories.get_by_id(fund_id)
        if not fund:
            return HttpResponse(status=406)
        if not fund.owner == user:
            return HttpResponse(status=400)
        fund.is_active = False
        try:
            fund.save()
        except(ValueError, AttributeError):
            return HttpResponse(status=400)
    return HttpResponse(f"You've just deleted: {fund.name}", status=200)

@require_http_methods(["POST"])
def fund_summary(request):
    """
    Handling request for getting summary info about fund.
        Args:
            request (HttpRequest) which consists fund_id
        Returns:
            JsonResponse object with summary info
    """
    fund_id = json.loads(request.body)['fund_id']
    fund = FundCategories.get_by_id(fund_id)
    fund_info = {'icon': fund.icon, 'name': fund.name}

    if fund.is_shared:
        fund_info['spend_group'] = SharedFunds.get_by_fund\
            (fund_id).group.name

    inc_history = total_value_for_category\
        (SpendingHistory.objects.filter(fund=fund_id), True)
    spend_history = total_value_for_category\
        (IncomeHistory.objects.filter(fund=fund_id), True)
    fund_info['total'] = inc_history['total'] - spend_history['total']
    last_value_info = total_category_validation(inc_history, spend_history)
    fund_info = {**last_value_info, **fund_info}
    print(fund_info)
    return JsonResponse(fund_info)
