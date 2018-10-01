"""
This module provides functions for spending specifying.
"""
import calendar
import json
from datetime import date
from django.http import HttpResponse, JsonResponse

from authentication.models import UserProfile
from .models import SpendingCategories, SpendingLimitationIndividual


def show_spending_ind(request, user_id=None):  #instead of user_id there should be request.user
    """Handling request for creating of spending categories list.

        Args:
            request (HttpRequest): Limitation data.
        Returns:
            HttpResponse object.
    """
    if request.method == "GET":
        if user_id:
            user = UserProfile.get_by_id(user_id)
            user_categories = []
            for entry in SpendingCategories.objects.filter(owner=user):
                user_categories.append({'id': entry.id, 'name': entry.name})
            return JsonResponse(user_categories, status=200, safe=False)
    return JsonResponse({}, status=400)


def set_spending_limitation_ind(request, user_id=2, spending_id=None):
    #instead of user_id there should be request.user
    """Handling request for create spending limitation.

        Args:
            request (HttpRequest): Limitation data.
        Returns:
            HttpResponse object.
    """
    if request.method == "POST":
        data = json.loads(request.body)
        data['month'] = int(data['month'])
        data['year'] = int(data['year'])
        data['value'] = float(data['value'])
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

        spending_limitation_ind.spending_category = SpendingCategories.get_by_id(spending_id)
        spending_limitation_ind.user = UserProfile.get_by_id(user_id)

        if SpendingLimitationIndividual.objects.filter\
            (user=spending_limitation_ind.user,
             spending_category=spending_limitation_ind.spending_category,
             start_date=spending_limitation_ind.start_date,
             finish_date=spending_limitation_ind.finish_date):
            SpendingLimitationIndividual.objects.filter\
                (user=spending_limitation_ind.user,
                 spending_category=spending_limitation_ind.spending_category,
                 start_date=spending_limitation_ind.start_date,
                 finish_date=spending_limitation_ind.finish_date).update(
                     value=round(float(data['value']), 2))
        else:
            spending_limitation_ind.value = round(float(data['value']), 2)
            spending_limitation_ind.save()

        return HttpResponse(status=201)
    else:
        return JsonResponse({}, status=400)
