"""
This module provides functions for spending specifying.
"""
import calendar
import json
from datetime import date

from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods

from group.models import Group, SharedSpendingCategories, UserProfile
from utils.validators import is_valid_data_individual_limit_fix, is_valid_data_new_spending, \
    is_valid_data_individual_limit_arb, date_parse
from utils.aws_helper import AwsService
from utils.universal_category_methods import total_value_for_category
from spending_history.models import SpendingHistory
from .models import SpendingCategories, SpendingLimitationIndividual, SpendingLimitationGroup

# CONSTANTS FOR ICONS
AWS_S3_URL = 'https://s3.amazonaws.com/family-finance-tracker-static/'
STANDARD_SPENDINGS_FOLDER = 'standard/'
ICON_FILE_NAME = 'miscellaneous.png'


@require_http_methods(["GET"])
def show_spending_ind(request):
    """Handling request for creating of spending categories list.

        Args:
            request (HttpRequest): Limitation data.
        Returns:
            HttpResponse object.
    """
    user = request.user
    icon_if_none = AWS_S3_URL + STANDARD_SPENDINGS_FOLDER + ICON_FILE_NAME
    if user:
        user_categories = []
        for entry in SpendingCategories.filter_by_user(user):
            url = AwsService.get_image_url(entry.icon) if entry.icon else icon_if_none
            user_categories.append({'id': entry.id, 'name': entry.name,
                                    'url': url})
        return JsonResponse({'categories': user_categories, 'fixed': user.ind_period_fixed},
                            status=200, safe=False)
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
    icon_if_none = AWS_S3_URL + STANDARD_SPENDINGS_FOLDER + ICON_FILE_NAME
    if user:
        for group in Group.filter_groups_by_user_id(user):
            for shared_category in SharedSpendingCategories.objects.filter(group=group.id):
                if shared_category.spending_categories.is_active:
                    icon = \
                        SpendingCategories.objects.get(
                            id=shared_category.spending_categories.id).icon  # pylint: disable=line-too-long
                    url = AwsService.get_image_url(icon) if icon else icon_if_none
                    users_group.append({'id_cat': shared_category.spending_categories.id,
                                        'name_cat': shared_category.spending_categories.name,
                                        'id_group': group.id,
                                        'name_group': group.name,
                                        'url': url
                                        })
        return JsonResponse(users_group, status=200, safe=False)
    return JsonResponse({}, status=400)


@require_http_methods(["POST"])
def set_limitation_period(request):
    """Handling request for defining limitation period.

        Args:
            request (HttpRequest): Type of period.
        Returns:
            HttpResponse object.
    """
    user = request.user
    data = json.loads(request.body)
    if data['fixed'] == 'null':
        return HttpResponse('Bad request', status=400)
    period_type = data['fixed']
    user.ind_period_fixed = period_type
    try:
        user.save()
    except(ValueError, AttributeError):
        return HttpResponse(status=406)
    response = "{} type of limitation period has been set...".format("Monthly/yearly"
                                                                     if period_type
                                                                     else "Arbitrary")
    return HttpResponse(response, status=201)


@require_http_methods(["POST"])
def set_spending_limitation_ind_fix(request):
    """Handling request for create spending limitation monthly/yearly.

        Args:
            request (HttpRequest): Limitation data.
        Returns:
            HttpResponse object.
    """
    user = request.user
    data = json.loads(request.body)
    if not is_valid_data_individual_limit_fix(data):
        return HttpResponse('Bad request', status=400)
    spending = SpendingCategories.get_by_id(int(data['spending_id']))
    if not spending:
        return HttpResponse('Bad request', status=400)
    month = int(data['month'])
    year = int(data['year'])
    value = round(float(data['value']), 2)

    if month:
        start_date = date(year, month, 1)
        finish_date = date(year, month, (calendar.monthrange(year, month))[1])
        year_limit = SpendingLimitationIndividual.get_value_by_data(user,
                                                                    spending,
                                                                    date(year, 1, 1),
                                                                    date(year, 12, 31))
        if year_limit:
            total_limit = - SpendingLimitationIndividual.get_value_by_data(
                user,
                spending,
                date(year, month, 1),
                date(year, month, (calendar.monthrange(year, month))[1]))
            for item in range(1, 13):
                total_limit += SpendingLimitationIndividual.get_value_by_data(
                    user,
                    spending,
                    date(year, item, 1),
                    date(year, item, (calendar.monthrange(year, item))[1]))
            if year_limit - total_limit < value:
                return HttpResponse(
                    "The yearly limit is {}, \n "
                    "the total monthly limit is {}.\n "
                    "Therefore, your limit {} can not be set.".format(
                        year_limit,
                        total_limit,
                        value), status=202)

    else:
        start_date = date(year, 1, 1)
        finish_date = date(year, 12, 31)
        total_limit = 0
        for item in range(1, 13):
            total_limit += SpendingLimitationIndividual.get_value_by_data(
                user,
                spending,
                date(year, item, 1),
                date(year, item, (calendar.monthrange(year, item))[1]))
        if total_limit > value:
            return HttpResponse(
                "The total monthly limit is {}. "
                "Therefore, your limit {} can not be set.".format(total_limit,
                                                                  value),
                status=202)

    spending_limitation = SpendingLimitationIndividual.filter_by_data(
        user,
        spending,
        start_date,
        finish_date)
    if spending_limitation:
        spending_limitation.update(value=value)
        response = "The limit {} has been updated...".format(value)
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
        response = "The limit {} has been set...".format(value)
    return HttpResponse(response, status=201)


@require_http_methods(["POST"])
def set_spending_limitation_ind_arb(request):
    """Handling request for create spending limitation arbitrary.

        Args:
            request (HttpRequest): Limitation data.
        Returns:
            HttpResponse object.
    """
    user = request.user
    data = json.loads(request.body)
    if not is_valid_data_individual_limit_arb(data):
        return HttpResponse('Bad request', status=400)
    spending = SpendingCategories.get_by_id(int(data['spending_id']))
    if not spending:
        return HttpResponse('Bad request', status=400)

    start_date, finish_date = date_parse(data)

    if start_date > finish_date:
        return JsonResponse({}, status=400)

    value = round(float(data['value']), 2)

    current_limit_ind = SpendingLimitationIndividual.objects.filter(
        Q(start_date__range=[start_date, finish_date]) |
        Q(finish_date__range=[start_date, finish_date])).filter(
            user=user,
            spending_category=spending)

    if current_limit_ind:
        return HttpResponse("The limit for these dates already exists. \n"
                            "Please change dates or category.",
                            status=202)
    spending_limitation_ind = SpendingLimitationIndividual(user=user,
                                                           spending_category=spending,
                                                           start_date=start_date,
                                                           finish_date=finish_date,
                                                           value=value)
    try:
        spending_limitation_ind.save()
    except(ValueError, AttributeError):
        return HttpResponse(status=406)
    return HttpResponse("The limit {} has been set...".format(value), status=201)


@require_http_methods(["GET"])
def check_dates_choice(request):
    """
    a function which checks if the user is a brand-new one who has not chosen the way of displaying
    date periods for setting group limits
    :param request
    :return: True - if the user already chose the way of displaying dates, otherwise - False
    """
    already_chosen = UserProfile.objects.filter(id=request.user.id).exclude(
        ind_period_fixed__isnull=False)
    if already_chosen:
        return HttpResponse(True, status=200)
    return HttpResponse(False, status=200)


@require_http_methods(["POST"])
def set_dates_choice(request):
    """
    the function which sets the way of displaying date periods for setting group limits
    :param request
    :return: HTTP status code 201
    """
    choice = json.loads(request.body)
    UserProfile.objects.filter(id=request.user.id).update(ind_period_fixed=choice['choice'])
    return HttpResponse(status=201)


def group_limit(request):
    """the functions finds all the shared spendings associated with particular user in the groups
    in which this user is an admin and returns them
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
        if not content['spending_category']:
            return HttpResponse('You did not choose any spending. Please choose it', status=400)
        if not content['start_date'] or not content['end_date'] or not content['value']:
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


@require_http_methods(["POST"])
def create_spending_category(request):
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
    owner = user
    is_shared = False

    if not is_valid_data_new_spending(data):
        return HttpResponse("Bad request", status=400)
    spending = SpendingCategories.filter_by_owner_name(owner=owner, name=name)

    if spending:
        return HttpResponse("Sorry, but such category exists...", status=202)

    spending = SpendingCategories(name=name, icon=icon, owner=owner, is_shared=is_shared)
    if not spending:
        return HttpResponse(status=406)
    spending.save()
    return HttpResponse("You've just created category '{}'.".format(name), status=201)


@require_http_methods(["DELETE"])
def delete_spending_category(request, spending_id):
    """Handling request for delete spending category.
        Args:
            request (HttpRequest): Data for delete category.
            spending_id: Spending category Id
        Returns:
            HttpResponse object.
    """
    user = request.user
    if user:
        spending = SpendingCategories.get_by_id(spending_id)
        if not spending:
            return HttpResponse(status=406)
        if not spending.owner == user:
            return HttpResponse(status=400)
        spending.is_active = False
        try:
            spending.save()
        except(ValueError, AttributeError):
            return HttpResponse(status=400)
    return HttpResponse(f"You've just deleted category: {spending.name}", status=200)


@require_http_methods(["POST"])
def spending_summary(request):
    """
    Handling request for getting summary info about spending category.
        Args:
            request (HttpRequest) which consists spending_id
        Returns:
            JsonResponse object with summary info
    """
    spend_id = json.loads(request.body)['spend_id']
    spend = SpendingCategories.get_by_id(spend_id)
    spend_info = {'icon': AwsService.get_image_url(spend.icon), 'name': spend.name}

    if spend.is_shared:
        spend_info['spend_group'] = SharedSpendingCategories.get_by_spending_id\
            (spend_id).group.name
    history = SpendingHistory.objects.filter(spending_categories_id=spend_id)
    spend_info = {**total_value_for_category(history, True), **spend_info}
    return JsonResponse(spend_info)
