"""
This module provides functions for handling spending_history view.
"""

import io
import json
import csv
from datetime import date, timedelta
from decimal import Decimal

from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from group.models import SharedSpendingCategories, Group, UsersInGroups, SharedFunds

from utils.get_role import groups_for_user, is_user_member_group, is_user_admin_group
from utils.spendings_limit_checker import compare_ind_spend_limit, comp_gr_spends_w_limit
from utils.validators import input_spending_registration_validate, is_valid_data_spending_history, \
    date_parse
from utils.download_history_file import creating_empty_xlsx_file, \
    file_streaming_response, spending_date_parser
from .models import SpendingCategories, SpendingHistory, FundCategories

@require_http_methods(["POST"])
def register_spending(request):
    """Handling request for creating of spending categories list.
        Args:
            request (HttpRequest): request from server which contain
            fund, category, sum, date, comment
        Returns:
            HttpResponse status.
    """
    data = json.loads(request.body)
    if not input_spending_registration_validate(data):
        return HttpResponse(status=400)
    user = request.user
    spending = SpendingCategories.get_by_id(int(data["category"]))
    fund = FundCategories.get_by_id(int(data["type_of_pay"]))
    if not spending and not fund:
        return HttpResponse(status=400)
    if spending.is_shared:
        if not SharedSpendingCategories.get_by_spending_id(spending.id):
            return HttpResponse(status=403)
    else:
        if not spending.owner == user:
            return HttpResponse(status=403)

    value = Decimal(data["value"])
    comment = data["comment"]

    spending_history = SpendingHistory(
        fund=fund,
        spending_categories=spending,
        date=data["date"],
        value=value,
        owner=user,
        comment=comment
    )
    try:
        spending_history.save()
    except(ValueError, AttributeError):
        return HttpResponse(status=406)
    response = f"You've just register spending {spending.name}. \n" +\
               compare_ind_spend_limit(user, data["date"], spending, value) + "\n" + \
               comp_gr_spends_w_limit(data['group_id'], data['category'])

    return HttpResponse(response, status=201)


def create_spending_history_individual(user, start_date, finish_date, utc_difference):
    """Creating array of data for individual spending history.
        Args:
            user (UserProfile): user.
            start_date (date): The beginning of statistic period
            finish_date (date): The end of statistic period
            utc_difference(int): difference between user's time and UTC
        Returns:
            Array of data for individual spending history statistic.
    """

    history_individual = []
    for entry in SpendingCategories.filter_by_user(user):
        history_individual_entry = []
        for item in SpendingHistory.filter_by_user_date_spending(user,
                                                                 start_date,
                                                                 finish_date,
                                                                 entry):
            history_individual_entry.append({'value': float(item.value),
                                             'date': (item.date +
                                                      timedelta(hours=utc_difference)).date(),
                                             'fund': item.fund.name})
        if history_individual_entry:
            history_individual.append({'spending': entry.name,
                                       'history': history_individual_entry})
    for group in groups_for_user(user):
        if is_user_member_group(group, user):
            for entry in SharedSpendingCategories.filter_by_group(group=group):
                history_individual_entry = []
                for item in SpendingHistory.filter_by_user_date_spending(user,
                                                                         start_date,
                                                                         finish_date,
                                                                         spending_categories=entry):
                    history_individual_entry.append({'value': float(item.value),
                                                     'date': (item.date +
                                                              timedelta(hours
                                                                        =utc_difference)).date(),
                                                     'fund': item.fund.name})
                if history_individual_entry:
                    history_individual.append({'spending': entry.name
                                                           + ' / '
                                                           + Group.get_group_by_id(group).name,
                                               'history': history_individual_entry})
    return history_individual


def create_spending_history_for_admin(user, start_date, finish_date, utc_difference):
    """Creating array of spending history data for admin.
        Args:
            user (UserProfile): user who needs information.
            start_date (date): The beginning of statistic period
            finish_date (date): The end of statistic period
        Returns:
            Array of spending history data for admin.
    """
    history_for_admin = []
    groups_for_admin = [group for group in groups_for_user(user)
                        if is_user_admin_group(group, user)]

    for group in groups_for_admin:

        for entry in SharedSpendingCategories.filter_by_group(group=group):

            history_spending_category = []

            for person in UsersInGroups.filter_by_group(group=group):
                history_person = []
                if is_user_member_group(group, person):
                    for item in SpendingHistory.filter_by_user_date_spending(person,
                                                                             start_date,
                                                                             finish_date,
                                                                             entry):
                        history_person.append({'member': person.email,
                                               'value': float(item.value),
                                               'date': (item.date +
                                                        timedelta(hours=utc_difference)).date(),
                                               'fund': 'Individual fund'})
                else:
                    for item in SpendingHistory.filter_by_user_date_spending(person,
                                                                             start_date,
                                                                             finish_date,
                                                                             entry):
                        fund_entry = item.fund.name \
                            if item.fund in SharedFunds.filter_by_group(group=group) \
                            else 'Individual fund'
                        history_person.append({'member': person.email,
                                               'value': float(item.value),
                                               'date': (item.date +
                                                        timedelta(hours=utc_difference)).date(),
                                               'fund': fund_entry})

                if history_person:
                    history_spending_category.extend(history_person)

            if history_spending_category:
                history_for_admin.append({'spending': entry.name
                                                      + ' / '
                                                      + Group.get_group_by_id(group).name,
                                          'history': history_spending_category})
    return history_for_admin


def create_xlsx(request):
    """
    Creating xlsx file with spending history for specific period
    Args:
        request (HttpRequest): request from server which contains
        user info and date params : start_date, finish_date, UTC
    Returns:
        StreamingHttpResponse xlsx file.
    """

    print(request)
    date_dict = spending_date_parser(request)

    individual_spending_history = create_spending_history_individual\
        (user=date_dict['user_id'],
         start_date=date_dict['start_date'],
         finish_date=date_dict['finish_date'],
         utc_difference=date_dict['utc_difference'])
    group_spending_history = create_spending_history_for_admin\
        (user=date_dict['user_id'],
         start_date=date_dict['start_date'],
         finish_date=date_dict['finish_date'],
         utc_difference=date_dict['utc_difference'])

    output, worksheet, workbook, formats_dict = creating_empty_xlsx_file()

    row, col = 2, 1

    if individual_spending_history:
        worksheet.write(row - 1, col, 'Individual spending', formats_dict['head_format'])
        for i in individual_spending_history[0]['history'][0]:
            worksheet.write(row - 1, col + 1, i, formats_dict['head_format'])
            col += 1

        col = 1
        for spending_dicts in individual_spending_history:
            for history_dict in spending_dicts['history']:
                worksheet.write(row, col, spending_dicts['spending'], formats_dict['cell_format'])
                worksheet.write_number\
                    (row, col + 1, history_dict['value'], formats_dict['value_format'])
                worksheet.write(row, col + 2, history_dict['date'], formats_dict['date_format'])
                worksheet.write(row, col + 3, history_dict['fund'], formats_dict['cell_format'])
                row += 1
    if group_spending_history:
        row = row + 1
        worksheet.write(row, col, 'Group spending', formats_dict['head_format'])
        for i in group_spending_history[0]['history'][0]:
            if i == 'member':
                worksheet.write(row, col - 1, 'Member', formats_dict['head_format'])
            else:
                worksheet.write(row, col + 1, i, formats_dict['head_format'])
                col += 1
        row, col = row + 1, 1
        for spending_dicts in group_spending_history:
            for history_dict in spending_dicts['history']:
                worksheet.write(row, col-1, history_dict['member'], formats_dict['cell_format'])
                worksheet.write(row, col, spending_dicts['spending'], formats_dict['cell_format'])
                worksheet.write_number\
                    (row, col + 1, history_dict['value'], formats_dict['value_format'])
                worksheet.write(row, col + 2, history_dict['date'], formats_dict['date_format'])
                worksheet.write(row, col + 3, history_dict['fund'], formats_dict['cell_format'])
                row += 1

    workbook.close()

    response = file_streaming_response \
        ('application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
         'spending_history.xlsx', output)
    return response

def create_csv(request):
    """
    Creating csv file with spending history for specific period
    Args:
        request (HttpRequest): request from server which contains
        user info and date params : start_date, finish_date, UTC
    Returns:
        StreamingHttpResponse csv file.
    """
    date_dict = spending_date_parser(request)

    individual_spending_history = create_spending_history_individual \
        (user=date_dict['user_id'],
         start_date=date_dict['start_date'],
         finish_date=date_dict['finish_date'],
         utc_difference=date_dict['utc_difference'])
    group_spending_history = create_spending_history_for_admin \
        (user=date_dict['user_id'],
         start_date=date_dict['start_date'],
         finish_date=date_dict['finish_date'],
         utc_difference=date_dict['utc_difference'])

    output = io.StringIO()

    if group_spending_history:
        headers = ['spending', 'group']
        for i in group_spending_history[0]['history'][0]:
            headers.append(i)
    elif individual_spending_history:
        headers = ['spending']
        for i in individual_spending_history[0]['history'][0]:
            headers.append(i)
    else:
        headers = []

    writer = csv.DictWriter(output, dialect='excel', quoting=csv.QUOTE_ALL, fieldnames=headers)
    writer.writeheader()

    if individual_spending_history:
        for spending_dicts in individual_spending_history:
            for i in spending_dicts['history']:
                i['spending'] = spending_dicts['spending']
            writer.writerows(spending_dicts['history'])

    if group_spending_history:
        for spending_dicts in group_spending_history:
            for i in spending_dicts['history']:
                i['spending'] = spending_dicts['spending'].split('/')[0]
                i['group'] = spending_dicts['spending'].split('/')[1]
            writer.writerows(spending_dicts['history'])

    response = file_streaming_response('text/csv', 'spending_history.csv', output)
    return response

@require_http_methods(["POST"])
def create_spending_history(request):
    """Handling request for creating spending history data.

        Args:
            request (HttpRequest): contains start date, final date and UTC information.
        Returns:
            JsonResponse object.
    """
    user = request.user
    data = json.loads(request.body)
    if not is_valid_data_spending_history(data):
        return HttpResponse(status=400)

    start_date, finish_date = date_parse(data)
    utc_difference = int(data['UTC'])
    if start_date > finish_date:
        return JsonResponse({}, status=400)

    if user:
        return JsonResponse({'individual':
                                 create_spending_history_individual(user,
                                                                    start_date,
                                                                    finish_date,
                                                                    utc_difference),
                             'admin':
                                 create_spending_history_for_admin(user,
                                                                   start_date,
                                                                   finish_date,
                                                                   utc_difference)},
                            status=200, safe=False)
    return JsonResponse({}, status=400)


@require_http_methods(["GET"])
def get_month_spending(request):
    """Handling request for representation total sum.
        Args:
            request (HttpRequest): data.
        Returns:
            HttpResponse object.
    """
    user = request.user
    finish_date = date.today()
    start_date = date(finish_date.year, finish_date.month, 1)

    if user:
        return HttpResponse(SpendingHistory.filter_by_user_date_spending(user,
                                                                         start_date,
                                                                         finish_date),
                            status=200)
    return HttpResponse('Bad Request', status=400)

def create_spending_chart(user, start_date, finish_date):
    """Creating array of data for spending history chart.
        Args:
            user (UserProfile): user.
            start_date (date): The beginning of statistic period
            finish_date (date): The end of statistic period
        Returns:
            Array of data for individual spending history statistic.
    """
    list_spending_value = list()
    list_spending_name = list()
    list_spending_id = list(set(SpendingHistory.filter_by_user_date(
        user,
        start_date,
        finish_date).values_list('spending_categories_id', flat=True)))
    for item in list_spending_id:
        list_spending_name.append(SpendingCategories.get_by_id(item).name)
        total = sum(SpendingHistory.filter_by_user_date_spending(
            user,
            start_date,
            finish_date,
            SpendingCategories.get_by_id(item)).values_list('value', flat=True))
        list_spending_value.append(total)
    return {'value': list_spending_value, 'name': list_spending_name}

@require_http_methods(["POST"])
def get_spending_chart(request):
    """Handling request for creating spending history data.

        Args:
            request (HttpRequest): contains start date, final date and UTC information.
        Returns:
            JsonResponse object.
    """
    user = request.user
    data = json.loads(request.body)
    if not is_valid_data_spending_history(data):
        return HttpResponse(status=400)
    start_date, finish_date = date_parse(data)

    if start_date > finish_date:
        return JsonResponse({}, status=400)

    if user:
        return JsonResponse(create_spending_chart(user, start_date, finish_date),
                            status=200, safe=False)
    return JsonResponse({}, status=400)
