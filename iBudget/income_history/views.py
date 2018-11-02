"""this module provides information about a customer's amount of incomes from the beginning of this
month till today and let a use track his incomes for the chose period of time
"""
import json
from datetime import datetime
import xlsxwriter
from decimal import Decimal
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.utils.dateparse import parse_datetime
from django.core.exceptions import ValidationError
from utils.validators import input_income_registration_validate
from .models import IncomeCategories, FundCategories, IncomeHistory




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
    """this function accepts dates and returns the list of incomes with the funds they went to,
    amounts, dates and comments
    """
    content = request.body
    content = json.loads(content)
    user_id = request.user
    if len(content) <= 1:
        return HttpResponse('You did not choose any dates or you chose only one date out of two',
                            status=400)
    time_diff = datetime.timedelta(hours=2)
    start_to_parse = content['start']
    end_to_parse = content['end']
    parsed_start = parse_datetime(start_to_parse) - time_diff
    parsed_end = parse_datetime(end_to_parse) - time_diff
    incomes_funds = IncomeHistory.objects.filter(date__range=(parsed_start, parsed_end),
                                                 income_id__owner_id=user_id)
    incomes_funds_ids = [
        {'income': i.income_id, 'fund': i.fund_id, 'date': str(i.date + time_diff)[:10],
         'amount': float(i.value), 'comment': i.comment} for i in incomes_funds]

    for counter in enumerate(incomes_funds_ids):
        incomes_funds_ids[counter[0]].update(
            {'income': IncomeCategories.objects.get(id=incomes_funds_ids[counter[0]]['income'])
                       .name})
        incomes_funds_ids[counter[0]].update(
            {'fund': FundCategories.objects.get(id=incomes_funds_ids[counter[0]]['fund']).name})
    print(incomes_funds_ids)
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

def create_xlsx():
    sample=[{'income': 'premiya', 'fund': 'something', 'date': '2018-10-29', 'amount': 1.2345, 'comment': '1'}, {'income': 'zarplata', 'fund': 'privat', 'date': '2018-10-31', 'amount': 100.0, 'comment': 'bilo delo'}, {'income': 'premiya',
    'fund': 'privat', 'date': '2018-10-29', 'amount': 5.0, 'comment': 'd'}, {'income': 'premiya', 'fund': 'kredo', 'date': '2018-10-28', 'amount': 123.0, 'comment': 'd'}]



    workbook = xlsxwriter.Workbook(r'demo.xlsx')
    worksheet = workbook.add_worksheet('Income_history')

    head_format = workbook.add_format({'bold': True, 'font_size': 12, 'align': 'center'})
    value_format = workbook.add_format({'num_format': '$#,##0'})
    date_format = workbook.add_format({'num_format': 'mmmm d yyyy'})
    worksheet.set_row(1, 20, head_format)

    head_row, head_col = 1, 1
    row, col = 2, 1
    for i in sample[0]:
        worksheet.write(head_row, head_col, i, head_format)
        head_col += 1

    for dicty in sample:
        for i in dicty:
            if i == 'amount':
                worksheet.write_number(row, col, dicty[i], value_format)
            elif i == 'date':
                date = datetime.strptime(dicty[i], "%Y-%m-%d")
                worksheet.write_datetime(row, col, date, date_format)
            else:
                worksheet.write(row, col, dicty[i])
            col += 1
        col = 1
        row += 1

    workbook.close()
