"""
This module provides functions for handling fund view.
"""
import json

from decimal import Decimal
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from group.models import Group, SharedFunds
from utils.validators import input_fund_registration_validate, date_range_validate, is_valid_data_create_new_fund
from utils.transaction import save_new_fund
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
    if is_valid_data_create_new_fund(data):
        return HttpResponse(status=400)
    user = request.user
    shared_group = data["shared_group"]
    is_shared = True if shared_group else False
    if save_new_fund(name=data["name"], icon=data["icon"], is_shared=is_shared, owner=user, shared_group=shared_group):
        return HttpResponse(status=201)
    return HttpResponse(status=406)
