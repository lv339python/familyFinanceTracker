"""this module provides information about a customer's amount of incomes from the beginning of this
month till today and let a use track his incomes for the chose period of time
"""
import json
import datetime
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.utils.dateparse import parse_datetime
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
    print(start_date)
    total = 0
    incomes_to_date = IncomeHistory.objects.filter(date__range=(start_date, end_date),
                                                   income_id__owner_id=user_id)

    if not incomes_to_date:
        return HttpResponse('There are no incomes during this period', status=204)
    print(incomes_to_date)

    for income in incomes_to_date:
        total = total+income.value
    print(total)
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
