"""this module provides information about a customer's amount of incomes from the beginning of this
month till today and let a use track his incomes for the chose period of time
"""
import csv
import datetime
import io
import json
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.http import JsonResponse, HttpResponse
from django.utils.dateparse import parse_datetime
from django.views.decorators.http import require_http_methods

from utils.download_history_file import creating_empty_xlsx_file, \
    file_streaming_response, income_date_parser
from utils.validators import input_income_registration_validate
from .models import IncomeCategories, FundCategories, IncomeHistory


def get_incomes_funds_ids(user_id, date_start, date_end, time_diff):
    """
    a function which accepts parameters defined in the function 'track'
    :return: list of all user's incomes, funds, dates, comments and sums within a chosen period
    """
    incomes_funds = IncomeHistory.objects.filter(date__range=(date_start, date_end),
                                                 income_id__owner_id=user_id)
    incomes_funds_ids = [
        {'income': i.income_id, 'fund': i.fund_id, 'date': str(i.date + time_diff)[:10],
         'amount': float(i.value), 'comment': i.comment, 'income_history_id':i.id} for i in incomes_funds
         if i.is_active]

    for counter in enumerate(incomes_funds_ids):
        incomes_funds_ids[counter[0]].update({'income': IncomeCategories.objects.get(
            id=incomes_funds_ids[counter[0]]['income']).name})
        incomes_funds_ids[counter[0]].update(
            {'fund': FundCategories.objects.get(id=incomes_funds_ids[counter[0]]['fund']).name})
    set_for_chart = set()
    for counter in enumerate(incomes_funds_ids):
        set_for_chart.add(incomes_funds_ids[counter[0]]['fund'])
    incomes_funds_ids.append(list(set_for_chart))
    return incomes_funds_ids


@require_http_methods(['GET'])
def show_total(request):
    """this function accepts request object and returns the amount of incomes from the beginning of
     this month till today
     """
    user_id = request.user
    end_date = datetime.datetime.utcnow()
    start_date = end_date.replace(day=1,
                                  hour=datetime.time(0, 0, 0).hour,
                                  minute=datetime.time(0, 0, 0).minute,
                                  second=datetime.time(0, 0, 0).second)
    total = 0
    incomes_to_date = IncomeHistory.objects.filter(date__range=(start_date, end_date),
                                                   income_id__owner_id=user_id)
    if not incomes_to_date:
        return HttpResponse(0, status=200)

    for income in incomes_to_date:
        total = total + income.value
    return HttpResponse(total, status=200)


@require_http_methods(['POST'])
def track(request):
    """
    Handling request for returning income history data.
    Args:
        request (HttpRequest): contains start date, final date and UTC information.
    Returns:
        JsonResponse object.
    """
    content = json.loads(request.body)
    user_id = request.user
    if len(content) <= 1:
        return HttpResponse('You did not choose any dates or you chose only one date out of two',
                            status=400)
    time_diff = datetime.timedelta(hours=content['time_diff'])
    parsed_start = parse_datetime(content['start']) - time_diff
    parsed_end = parse_datetime(content['end']) - time_diff
    incomes_funds_ids = get_incomes_funds_ids(user_id=user_id,
                                              date_start=parsed_start,
                                              date_end=parsed_end,
                                              time_diff=time_diff)

    return JsonResponse(incomes_funds_ids, safe=False, status=200)


@require_http_methods(["POST"])
def register_income(request):
    """
    Handling request for creating of income categories list.
    Args:
        request (HttpRequest): request from server which contains
        income category, fund category, value, date, comment
    Returns:
        HttpResponse status.
    """
    data = json.loads(request.body)
    if not input_income_registration_validate(data):
        return HttpResponse('Please, fill all required fields properly !', status=400)

    income = IncomeCategories.get_by_id(int(data["inc_category"]))
    if not income:
        return HttpResponse(status=400)
    fund = FundCategories.get_by_id(int(data["fund_category"]))
    if not fund:
        return HttpResponse(status=400)
    date = data["date"]
    value = Decimal(data["value"])
    comment = data["comment"]

    income_history = IncomeHistory(
        fund=fund,
        income=income,
        date=date,
        value=value,
        comment=comment
    )
    try:
        income_history.save()
    except(ValueError, AttributeError, ValidationError):
        return HttpResponse('Check all required fields', status=406)
    return HttpResponse('Your income was successfully registered', status=201)


def create_xlsx(request):
    """
    Creating xlsx file with income history for specific period
    Args:
        request (HttpRequest): request from server which contains
        user info and date params : start_date, finish_date, UTC
    Returns:
        StreamingHttpResponse xlsx file.
    """

    date_dict = income_date_parser(request)

    income_history = get_incomes_funds_ids(user_id=date_dict['user_id'],
                                           date_start=date_dict['start_date'],
                                           date_end=date_dict['finish_date'],
                                           time_diff=date_dict['utc_difference'])
    del income_history[-1]

    output, worksheet, workbook, formats_dict = creating_empty_xlsx_file()

    if income_history:
        head_row, head_col = 1, 1
        row, col = 2, 1
        for i in income_history[0]:
            worksheet.write(head_row, head_col, i, formats_dict['head_format'])
            head_col += 1

        for history_dict in income_history:
            for i in history_dict:
                if i == 'amount':
                    worksheet.write_number(row, col, history_dict[i], formats_dict['value_format'])
                elif i == 'date':
                    date = datetime.datetime.strptime(history_dict[i], "%Y-%m-%d")
                    worksheet.write_datetime(row, col, date, formats_dict['date_format'])
                else:
                    worksheet.write(row, col, history_dict[i], formats_dict['cell_format'])
                col += 1
            col = 1
            row += 1

    workbook.close()

    response = file_streaming_response \
        ('application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
         'income_history.xlsx', output)
    return response


def create_csv(request):
    """
    Creating csv file with income history for specific period
    Args:
        request (HttpRequest): request from server which contains
        user info and date params : start_date, finish_date, UTC
    Returns:
        StreamingHttpResponse csv file.
    """
    date_dict = income_date_parser(request)

    income_history = get_incomes_funds_ids(user_id=date_dict['user_id'],
                                           date_start=date_dict['start_date'],
                                           date_end=date_dict['finish_date'],
                                           time_diff=date_dict['utc_difference'])
    del income_history[-1]

    output = io.StringIO()

    headers = []
    if income_history:
        for i in income_history[0]:
            headers.append(i)

    writer = csv.DictWriter(output, dialect='excel', quoting=csv.QUOTE_ALL, fieldnames=headers)
    writer.writeheader()

    if income_history:
        writer.writerows(income_history)

    response = file_streaming_response('text/csv', 'income_history.csv', output)
    return response

@require_http_methods(["DELETE"])
def delete_income_history(request, income_history_id):
    """Handling request for delete income history.
        Args:
            request (HttpRequest): Data for delete income history.
            income_history_id: Income History Id
        Returns:
            HttpResponse object.
    """
    user = request.user
    income_history = IncomeHistory.get_by_id(income_history_id)
    if not income_history:
        return HttpResponse(status=406)
    if not income_history.income.owner == user:
        return HttpResponse(status=400)
    income_history.update(is_active=False)
    return HttpResponse("You've just deleted this income from your history", status=200)
