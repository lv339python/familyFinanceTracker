"""
This module provides functions for spending specifying.
"""
import calendar
import json
from datetime import date
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods

from .models import SpendingCategories, SpendingLimitationIndividual, UserProfile


@require_http_methods(["GET"])
def show_spending_ind(request):
    """Handling request for creating of spending categories list.

        Args:
            request (HttpRequest): Limitation data.
        Returns:
            HttpResponse object.
    """
    #user = request.user
    user = UserProfile.get_by_id(5)
    if user:
        user_categories = []
        for entry in SpendingCategories.filter_by_id(user, False):
            user_categories.append({'id': entry.id, 'name': entry.name})
        return JsonResponse(user_categories, status=200, safe=False)
    return JsonResponse({}, status=400)


@require_http_methods(["POST"])
def set_spending_limitation_ind(request):
    """Handling request for create spending limitation.

        Args:
            request (HttpRequest): Limitation data.
        Returns:
            HttpResponse object.
    """
    user = request.user
    data = json.loads(request.body)
    data['spending_id'] = int(data['spending_id'])
    data['month'] = int(data['month'])
    data['year'] = int(data['year'])
    data['value'] = round(float(data['value']), 2)

    spending_limitation_ind = SpendingLimitationIndividual()
    if data['month']:
        spending_limitation_ind.start_date = date(data['year'], data['month'], 1)
        spending_limitation_ind.finish_date = date(data['year'],
                                                   data['month'],
                                                   (calendar.monthrange(data['year'],
                                                                        data['month']))[1])
    else:
        spending_limitation_ind.start_date = date(data['year'], 1, 1)
        spending_limitation_ind.finish_date = date(data['year'], 12, 31)

    spending_limitation_ind.spending_category = \
        SpendingCategories.get_by_id(data['spending_id'])

    spending_limitation = SpendingLimitationIndividual.objects.filter(
        user=user,
        spending_category=spending_limitation_ind.spending_category,
        start_date=spending_limitation_ind.start_date,
        finish_date=spending_limitation_ind.finish_date)
    if spending_limitation:
        spending_limitation.update(value=data['value'])
    else:
        spending_limitation_ind.value = data['value']
        spending_limitation_ind.user = user
        spending_limitation_ind.save()

    return HttpResponse(status=201)
