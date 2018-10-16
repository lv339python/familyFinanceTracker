"""
This module provides functions for handling fund view.
"""
import json

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import FundCategories
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

@require_http_methods(["GET"])
def show_goal_data(request):
    user = request.user
    if user:
        user_goal_statistic = []
        for entry in FundCategories.filter_by_user(user):
            for item in IncomeHistory.filter_by_fund_id(entry.id):
                user_goal_statistic.append({'date':item.date, "value":item.value})
        return JsonResponse(user_goal_statistic, status=200, safe=False)
    return JsonResponse({}, status=400)
