"""
This module provides functions for spending specifying.
"""
import calendar
import json
from datetime import date
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods

from .models import SpendingCategories, SpendingLimitationIndividual

import json
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from authentication.models import UserProfile
from group.models import Group, UsersInGroups, SharedSpendingCategories
from .models import SpendingCategories

# @require_http_methods(["POST"])
# def set_shared_create(request):
#
#   data=json.loads(request.body)
#   is_shared = bool(data["is_shared"])
#   name = data["name"]
#   icon = data["icon"]
#   owner = data["owner"]
#   # owner = UserProfile.get_by_id(owner)
#   category=SpendingCategories.get_category(request, name=name)
#   if  not category:
#     SpendingCategories.create(name, icon, owner, is_shared)
#     return JsonResponse(status=201)
#   return JsonResponse("This category is alredy use", status=400)
#
# @require_http_methods(["PUT"])
# def set_shared_update(request):
#
#     data = json.loads(request.body)
#     is_shared = bool(data["is_shared"])
#     name = data["name"]
#     icon = data["icon"]
#     owner = data["owner"]
#     owner = UserProfile.get_by_id(owner)
#     category = SpendingCategories.get_category(request, name=name)
#     if category:
#       SpendingCategories.update(name, icon, owner, is_shared)
#       return JsonResponse(status=201, safe=False)
#     return JsonResponse("This category is alredy use", status=400)


@require_http_methods(["GET"])
def show_spending(request):
    user = request.user
    if user:
        user_categories = []
        for entry in SpendingCategories.objects.filter(owner=user, is_shared=True):
            user_categories.append({'id': entry.id, 'name': entry.name})
        return JsonResponse(user_categories, status=200, safe=False)
    return JsonResponse({}, status=400)






# @require_http_methods(["GET"])
# def show_spending_ind(group_id):
#     """Handling request for creating of spending categories list.
#         Args:
#             request (HttpRequest): Limitation data.
#         Returns:
#             HttpResponse object.
#     """
#
#
#
#
#     group = Group.get_by_id(group_id)
#
#     if group:
#       group_category = []
#       for entry in SpendingCategories.objects.filter(id=SharedSpendingCategories.get_spend_by_group(group).id):
#         group_category.append({'id': entry.id, 'name': entry.name})
#
#         print(group_category)
#       return JsonResponse(group_category, status=200, safe=False)
@require_http_methods(["GET"])
def show_spending_ind(request):

    user = request.user
    # user = UserProfile.get_by_id(1)
    users_group = []

    if user:
        for i in Group.objects.filter(owner = user):
            group_id = i.id
            for el in SharedSpendingCategories.objects.filter(group = group_id):
                users_group.append({'id_cat': el.id,
                                    'name_cat': el.spending_categories.name,
                                    'id_group': group_id
                                    })
    return JsonResponse(users_group, status=200, safe=False)



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
