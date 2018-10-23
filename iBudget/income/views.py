"""
This module provides functions for spending specifying.
"""
import calendar
import json
from datetime import date
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Q

from utils.validators import is_valid_data_individual_limit, is_valid_data_new_spending
from group.models import Group, SharedSpendingCategories
from .models import IncomeCategories


@require_http_methods(["GET"])
def show_income_ind(request):
    """Handling request for creating of spending categories list.

        Args:
            request (HttpRequest): Limitation data.
        Returns:
            HttpResponse object.
    """
    user = request.user
    if user:
        user_categories = []
        for entry in IncomeCategories.filter_by_user(user):
            user_categories.append({'id': entry.id, 'name': entry.name})
        return JsonResponse(user_categories, status=200, safe=False)
    return JsonResponse({}, status=400)

@require_http_methods(["GET"])
def show_income_group(request):
    """Handling request for creating of spending categories list in group.
        Args:
            request (HttpRequest): Limitation data.
        Returns:
            HttpResponse object.
    """

    user = request.user
    users_funds = []
    if user:
        for group in Group.filter_groups_by_user_id(user):
            for shared_fund in Group.filter_funds_by_group(group):
                users_funds.append({'id_fund': shared_fund['id'],
                                    'name_fund': shared_fund['name'],
                                    'id_group': group.id,
                                    'group_name': group.name
                                    })
        return JsonResponse(users_funds, status=200, safe=False)
    return JsonResponse({}, status=400)
