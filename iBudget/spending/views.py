"""
This module provides functions for spending specifying.
"""
import calendar
import json
from datetime import date
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from utils.validators import is_valid_data_individual_limit
from group.models import Group, SharedSpendingCategories
from .models import SpendingCategories, SpendingLimitationIndividual, SpendingLimitationGroup


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
        for entry in SpendingCategories.filter_by_user(user):
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
            for shared_category in SharedSpendingCategories.objects.filter(group=group.id):
                users_group.append({'id_cat': shared_category.spending_categories.id,
                                    'name_cat': shared_category.spending_categories.name,
                                    'id_group': group.id
                                    })
        return JsonResponse(users_group, status=200, safe=False)
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
    if not is_valid_data_individual_limit(data):
        return HttpResponse(status=400)
    spending = SpendingCategories.get_by_id(int(data['spending_id']))
    if not spending:
        return HttpResponse(status=400)
    month = int(data['month'])
    year = int(data['year'])
    value = round(float(data['value']), 2)

    if month:
        start_date = date(year, month, 1)
        finish_date = date(year, month, (calendar.monthrange(year, month))[1])
    else:
        start_date = date(year, 1, 1)
        finish_date = date(year, 12, 31)

    spending_limitation = SpendingLimitationIndividual.filter_by_data(
        user,
        spending,
        start_date,
        finish_date)
    if spending_limitation:
        spending_limitation.update(value=value)
    else:
        spending_limitation_ind = SpendingLimitationIndividual(user=user,
                                                               spending_category=spending,
                                                               start_date=start_date,
                                                               finish_date=finish_date,
                                                               value=value)
        try:
            spending_limitation_ind.save()
        except(ValueError, AttributeError):
            return HttpResponse(status=406)

    return HttpResponse(status=201)


def group_limit(request):
    """the functions finds all the shared spendings associated with particular user and
    returns them
    :param request object
    """
    if request.method == 'GET':
        user_id = request.user
        available_spendings = SpendingCategories.objects.filter(
            sharedspendingcategories__group__usersingroups__user_id=
            user_id,
            sharedspendingcategories__group__usersingroups__is_admin=
            True).distinct('name')
        list_of_spendings = []
        for i in available_spendings:
            list_of_spendings.append(i.name)
        return JsonResponse(list_of_spendings, safe=False, status=200)
    return HttpResponse('Wrong request method', status=405)


def set_group_limit(request):
    """the function sets a limit for particular group and checks if such limit already
    exists
    :params:
    request object with JSON in its body
    """
    if request.method == 'POST':
        content = request.body
        content = json.loads(content)
        if content['spending_category'] == '':
            return HttpResponse('You did not choose any spending. Please choose it', status=400)
        if content['start_date'] == '' or content['end_date'] == '' or content['value'] == '':
            return HttpResponse('You did not fill all the required fields. Please fill them!',
                                status=400)
        instance = SpendingCategories.objects.get(name=content['spending_category'])
        catgs_with_limits = []
        current_limitdates = \
            SpendingLimitationGroup.objects.filter(Q(start_date__range=(content['start_date'],
                                                                        content['end_date'])) | Q
                                                   (end_date__range=(content['start_date'],
                                                                     content['end_date'])))
        if current_limitdates:
            for i in current_limitdates:
                catgs_with_limits.append(i.spending_category_id)
                if instance.id in catgs_with_limits:
                    return HttpResponse(
                        "The limit for category '{}' already exists. Change limit?".format(
                            instance.name), status=202)

            return HttpResponse("The limit for these dates already exists. Please change dates.",
                                status=202)
        SpendingLimitationGroup.objects.create(spending_category=instance,
                                               start_date=
                                               content['start_date'],
                                               end_date=content['end_date'],
                                               value=content['value'])
        return HttpResponse("Limit for spending '{}' is set".format(instance.name), status=200)
    return HttpResponse('Wrong request method', status=405)


def change_group_limit(request, category_name):
    """When user clicks 'yes' to change the limit the URL 'admin/change_limit/<int: category_id>/
    is opened and this function allows to set the new limit to the current limit.
    params:
    category_name: keyword argument (string)
    """
    if request.method == 'POST':
        content = request.body
        content = json.loads(content)
        new_limit = content['value']
        spending_to_find = SpendingCategories.objects.get(name=category_name)
        SpendingLimitationGroup.objects.filter(spending_category_id=spending_to_find.id). \
            update(value=new_limit)
        return HttpResponse("The limit amount has been changed to  '{}'".format(new_limit))
    return HttpResponse('Wrong request method', status=405)

# Addition to Halya, getting available standard images

