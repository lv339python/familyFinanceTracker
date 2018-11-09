"""
This module provides functions for income specifying.
"""
import json

from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from group.models import Group
from income_history.models import IncomeHistory
from utils.validators import is_valid_data_new_income
from .models import IncomeCategories


@require_http_methods(["POST"])
def create_category(request):
    """Handling request for creating new spending category.

        Args:
            request (HttpRequest): Data for new category.
        Returns:
            HttpResponse object.
    """
    user = request.user
    data = json.loads(request.body)

    name = data['name']
    icon = data['icon']
    date = data["date"]
    value = int(data["value"])
    owner = user

    if not is_valid_data_new_income(data):
        return HttpResponse("Bad request", status=400)
    income = IncomeCategories.filter_by_owner_name(owner=owner, name=name)

    if income:
        return HttpResponse("Sorry, but such category exists...\n OK", status=202)

    income = IncomeCategories(name=name, icon=icon, date=date, value=value, owner=owner)
    if not income:
        return HttpResponse(status=406)
    income.save()
    return HttpResponse("You've just created category '{}'. \n OK".format(name), status=201)

@require_http_methods(["GET"])
def show_income_ind(request):
    """
    Handling request for creating list of users incomes.
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
    """
    Handling request for creating list of funds for specific group.
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


@require_http_methods(["DELETE"])
def delete_income(request, income_category_id):
    """Handling request for delete income.
        Args:
            request (HttpRequest): Data for delete income.
            income_category_id: IncomeCategories Id
        Returns:
            HttpResponse object.
    """
    user = request.user
    income = IncomeCategories.get_by_id(income_category_id)
    if not income:
        return HttpResponse(status=406)
    if not income.owner == user:
        return HttpResponse(status=400)
    income.update(is_active=False)
    return HttpResponse(f"You've just deleted income {income.name}", status=200)
