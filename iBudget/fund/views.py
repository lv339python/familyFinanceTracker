"""
This module provides functions for handling fund view.
"""
import json

from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from .models import FundCategories, FinancialGoal
from income_history.models import IncomeHistory


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


def list_goal_user(user):
    user = 1
    list_fund =[]
    for entry in FundCategories.filter_by_user(user):
        list_fund.append(entry.id)
    list_goal = []
    for entry in list_fund:
        financial_goal=FinancialGoal.objects.filter(fund=entry)
        if financial_goal:
            list_goal.append(entry)
    return list_goal




@require_http_methods(["GET"])
def show_goal_data(request):
    user = request.user
    user = 1
    if user:
        user_goal_statistic = []
        for entry in list_goal_user(user):
            fund_category= FundCategories.get_by_id(entry)
            list_transactions = []
            for item in IncomeHistory.objects.filter(fund=entry, date__range=[fund_category.goal.start_date,fund_category.goal.finish_date]):
                list_transactions.append(item.value)
            user_goal_statistic.append({"id": entry, "name": fund_category.name,"value": fund_category.goal.value,"start_date":fund_category.goal.start_date,"finish_date":fund_category.goal.finish_date,
                                        'transaction': list_transactions})
        return HttpResponse(user_goal_statistic, status=200)
    return JsonResponse({}, status=400)


