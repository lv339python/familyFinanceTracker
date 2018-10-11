"""
This module provides functions for spending specifying.
"""
import calendar
import json
from datetime import date
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods

from utils.validators import spending_individual_limit_validate
from .models import SpendingCategories, SpendingLimitationIndividual

from django.db.models import Q
from utils.spendings_limit_checker import comp_gr_spends_w_limit # pylint: disable=W0611

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


def group_limit(request):
    """the functions finds all the shared spendings associated with particular user and
    returns them
    :param request object
    """
    if request.method == 'GET':
        user_id = request.user
        available_spendings = \
        SpendingCategories.objects.filter(sharedspendingcategories__group__usersingroups__user_id=
                                          user_id,
                                          sharedspendingcategories__group__usersingroups__is_admin=
                                          True).distinct('name')
        list_of_spensings = []
        for i in available_spendings:
            list_of_spensings.append(i.name)
        return JsonResponse(list_of_spensings, safe=False, status=200)
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
        print(len(current_limitdates))
        if current_limitdates:
            for i in current_limitdates:
                catgs_with_limits.append(i.spending_category_id)
                if instance.id in catgs_with_limits:
                    return HttpResponse(
                        "The limit for category '{}' already exists. Change limit?".format(
                            instance.name), status=202)

            return HttpResponse("The limit for these dates already exists. Please change dates.",
                                status=202)
        SpendingLimitationGroup.objects.create(spending_category=instance, start_date=
                                               content['start_date'], end_date=content['end_date'],
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
        SpendingLimitationGroup.objects.filter(spending_category_id=spending_to_find.id).\
                                          update(value=new_limit)
        return HttpResponse("The limit amount has been changed to  '{}'".format(new_limit))
    return HttpResponse('Wrong request method', status=405)
