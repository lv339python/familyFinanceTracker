"""
This module provides functions for handling fund view.
"""
from django.http import JsonResponse
from datetime import date
import calendar
import json
from decimal import Decimal

from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from group.models import Group, SharedFunds
from utils.validators import input_spending_registration_validate
from .models import FundCategories,  FinancialGoal


@require_http_methods(["GET"])
def show_spending_ind(request):
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
def show_fund_group(request):
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
def register_financial_goal_group(request):
    """Handling request for creating of funis_valid_data_individual_limit(data):
        return HttpResponse(status=400)
    spending = SpendingCategories.get_by_id(int(data['spending_id']))
    if not spending:
        return HttpResponse(status=400)
    month = int(data['month'])
    year = int(data['year'])
    value = round(float(data['value']), 2)
d list.
        Args:
            request (HttpRequest): request from server which contain
            value, start date, finish date
        Returns:
            HttpResponse status.
    """
    data = json.loads(request.body)
    # if not input_spending_registration_validate(data):
    #     return HttpResponse(status=400)
    user = request.user
    fund = FundCategories.get_by_id(int(data["fund"]))
    if not fund.owner == user:
        return HttpResponse(status=403)
    # month = int(data['month'])
    # year = int(data['year'])
    value = Decimal(data["value"])

    # if month:
    #     start_date = date(year, month, 1)
    #     finish_date = date(year, month, (calendar.monthrange(year, month))[1])
    # else:
    #     start_date = date(year, 1, 1)
    #     finish_date = date(year, 12, 31)
    #
    # financial_goal = FinancialGoal.filter_by_data(
    #     start_date,
    #     finish_date,
    #     fund)
    # if financial_goal:
    #     financial_goal.update(value=value)
    # else:
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

