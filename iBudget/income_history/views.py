"""this module provides information about a customer's amount of incomes from the beginning of this
month till today and let a use track his incomes for the chose period of time
"""
import json
import datetime
from decimal import Decimal
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.utils.dateparse import parse_datetime
from django.core.exceptions import ValidationError
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
        return HttpResponse(0, status=200)

    for income in incomes_to_date:
        total = total+income.value
    return HttpResponse(total, status=200)


@require_http_methods(['POST'])
def track(request):
    """this function accepts dates and returns the list of incomes with the funds they went to,
    amounts, dates and comments
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
