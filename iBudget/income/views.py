"""
This module provides functions for income specifying.
"""
import json

from django.http import HttpResponse
from django.views.decorators.http import require_http_methods

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

    income = IncomeCategories.create(name=name, icon=icon, date=date, value=value, owner=owner)
    if not income:
        return HttpResponse(status=406)
    return HttpResponse("You've just created category '{}'. \n OK".format(name), status=201)
