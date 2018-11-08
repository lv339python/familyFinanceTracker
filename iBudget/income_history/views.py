"""this module provides information about a customer's amount of incomes from the beginning of this
month till today and let a use track his incomes for the chose period of time
"""
import io
import json
import xlsxwriter
import datetime
import csv

from decimal import Decimal
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.utils.dateparse import parse_datetime
from django.core.exceptions import ValidationError
from utils.validators import input_income_registration_validate
from .models import IncomeCategories, FundCategories, IncomeHistory
from django.http import StreamingHttpResponse


def get_incomes_funds_ids(user_id, date_start, date_end, time_diff):
    """
    Getting income history information.
    Args:
        user_id , start date, final date and UTC information.
    Returns:
        dictionary with income history info
    """
    incomes_funds = IncomeHistory.objects.filter(date__range=(date_start, date_end),
                                                 income_id__owner_id=user_id)
    incomes_funds_ids = [
        {'income': i.income_id, 'fund': i.fund_id, 'date': str(i.date + time_diff)[:10],
         'amount': float(i.value), 'comment': i.comment} for i in incomes_funds]

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
        return HttpResponse('There are no incomes during this period', status=204)

    for income in incomes_to_date:
        total = total+income.value
    return HttpResponse(total)


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
    time_diff = datetime.timedelta(hours=2)
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
    output = io.BytesIO()

    user = request.user
    start_date = parse_datetime(request.GET['start_date'])
    finish_date = parse_datetime(request.GET['finish_date'])
    utc = int(request.GET['UTC'])
    utc_difference = datetime.timedelta(hours=utc)

    income_history = get_incomes_funds_ids(user, start_date, finish_date, utc_difference)
    del income_history[-1]

    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet('history')

    head_format = workbook.add_format({'bold': True, 'font_size': 12, 'align': 'center', 'border': 5})
    value_format = workbook.add_format({'num_format': '$#.#0', 'align': 'center', 'border': 1})
    date_format = workbook.add_format({'num_format': 'mmmm d yyyy', 'align': 'center', 'border': 1})
    cell_format = workbook.add_format({'align': 'center', 'border': 1})
    worksheet.set_column(0, 5, 20)

    if income_history:
        head_row, head_col = 1, 1
        row, col = 2, 1
        for i in income_history[0]:
            worksheet.write(head_row, head_col, i, head_format)
            head_col += 1

        for history_dict in income_history:
            for i in history_dict:
                if i == 'amount':
                    worksheet.write_number(row, col, history_dict[i], value_format)
                elif i == 'date':
                    date = datetime.datetime.strptime(history_dict[i], "%Y-%m-%d")
                    worksheet.write_datetime(row, col, date, date_format)
                else:
                    worksheet.write(row, col, history_dict[i], cell_format)
                col += 1
            col = 1
            row += 1

    workbook.close()

    output.seek(0)

    filename = 'income_history.xlsx'
    response = StreamingHttpResponse(
        output,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
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
    user = request.user
    start_date = parse_datetime(request.GET['start_date'])
    finish_date = parse_datetime(request.GET['finish_date'])
    utc = int(request.GET['UTC'])
    utc_difference = datetime.timedelta(hours=utc)

    income_history = get_incomes_funds_ids(user, start_date, finish_date, utc_difference)
    del income_history[-1]

    output = io.StringIO()

    headers = []
    if income_history:
        [headers.append(i) for i in income_history[0]]

    writer = csv.DictWriter(output, dialect='excel', quoting=csv.QUOTE_ALL, fieldnames=headers)
    writer.writeheader()

    if income_history:
        writer.writerows(income_history)

    output.seek(0)
    response = HttpResponse(output, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=income_history.csv'

    return response
