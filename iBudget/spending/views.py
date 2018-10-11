"""
This module provides functions for spending specifying.
"""
import calendar
import json
from datetime import date
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods

from utils.validators import spending_individual_limit_validate
from group.models import Group, SharedSpendingCategories
from .models import SpendingCategories, SpendingLimitationIndividual



@require_http_methods(["GET"])
def show_spending_ind(request):
    """Handling request for creating of spending categories list.

        Args:
            request (HttpRequest): Limitation data.
        Returns:
            HttpResponse object.
    """
    user = request.user
    if user:
        user_categories = []
        for entry in SpendingCategories.get_by_user_ind(user):
            user_categories.append({'id': entry.id, 'name': entry.name})
        return JsonResponse(user_categories, status=200, safe=False)
    return JsonResponse({}, status=400)




@require_http_methods(["GET"])
def show_spending_group(request):
    """Handling request for creating of spending categories list in group.
        Args:
            request (HttpRequest): Limitation data.
        Returns:
            HttpResponse object.
    """

    user = request.user
    users_group = []

    if user:
        for group in Group.group_filter_by_owner_id(user):
            group_id = group.id
            print(group.id)
            for shared_category in SharedSpendingCategories.objects.filter(group=group_id).order_by("spending_categories_id"):
                users_group.append({'id_cat': shared_category.spending_categories.id,
                                    'name_cat': shared_category.spending_categories.name,
                                    'id_group': group_id
                                    })
            print(SharedSpendingCategories.objects.filter(group=group_id))
        return JsonResponse(users_group, status=200, safe=False)
    return JsonResponse({}, status=400)

    # for group in Group.group_filter_by_owner_id(user):
    #     users_group.append({'id': group.id})
    # for cat in SpendingCategories.get_by_user_ind(user):
    #     users_group.append({"id": cat.id, "name": cat.name})
    # print(users_group)












# @require_http_methods(["GET"])
# def show_spending_group(request):
#     """Handling request for creating of spending categories list in group.
#         Args:
#             request (HttpRequest): Limitation data.
#         Returns:
#             HttpResponse object.
#     """
#
#     user = request.user
#     # users_group = []
#
#     if user:
#         # spendings_by_group=\
#         # SpendingCategories.objects.filter(sharedspendingcategories__group__usersingroups__user_id=1)
#         # print(spendings_by_group)
#         list_of_spendings=[]
#         # for spendings in spendings_by_group:
#         #     list_of_spendings.append({'id_cat': spendings.SpendingCategories.id,
#         #                             'name_cat': spendings.SpendingCategories.name,
#                                     # 'id_group': spendings.
#                                     # })
#
#         for group in Group.group_filter_by_owner_id(user):
#             group_id = group.id
#              for shared_category in SharedSpendingCategories.objects.filter(group=group_id):
#                 users_group.append({'id_cat': shared_category.id,
#                                     'name_cat': shared_category.spending_categories.name,
#                                     'id_group': group.group_id
#                                     })
#         print(list_of_spendings)
#              return JsonResponse(list_of_spendings, status=200, safe=False)
#         return JsonResponse({}, status=400)


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
    if not spending_individual_limit_validate(data):
        return HttpResponse(status=201)
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

    spending_limitation = SpendingLimitationIndividual.get_by_data(
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
