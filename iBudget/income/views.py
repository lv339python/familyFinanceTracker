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
