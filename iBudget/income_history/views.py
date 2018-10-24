from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
import json
from .models import IncomeCategories, FundCategories, IncomeHistory
import datetime
from django.utils.dateparse import parse_datetime

require_http_methods(['GET'])
def show_total(request):
    user_id = request.user
    ukr_time_diff = datetime.timedelta(hours=3)
    end_date = datetime.datetime.utcnow()
    start_date = end_date.replace(day=1,
                                  hour=datetime.time(0,0,0).hour,
                                  minute=datetime.time(0,0,0).minute,
                                  second=datetime.time(0,0,0).second)
    print(start_date)
    total = 0
    incomes_to_date = IncomeHistory.objects.filter(date__range=(start_date, end_date), income_id__owner_id=user_id)

    if not incomes_to_date:
        return HttpResponse('There are no incomes during this period', status=204)
    print(incomes_to_date)

    for income in incomes_to_date:
        total = total+income.value
    print(total)
    return HttpResponse(total)



@require_http_methods(['POST'])
def track(request):
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
    # dict_of_incomes_funds = []
    # for i in incomes_funds:
    #     print(i.date)
    # print(incomes_funds_ids)
    for n in range(len(incomes_funds_ids)):
        # list_of_incomes_funds.append({IncomeCategories.objects.get(id=incomes_funds_ids[n]
        # ['income']).name :
        #               FundCategories.objects.get(id=incomes_funds_ids[n]['fund']).name})
        incomes_funds_ids[n].update(
            {'income': IncomeCategories.objects.get(id=incomes_funds_ids[n]['income']).name})
        incomes_funds_ids[n].update(
            {'fund': FundCategories.objects.get(id=incomes_funds_ids[n]['fund']).name})

    print(incomes_funds_ids)

    # for l in dict_of_incomes_funds:
    #     for k,v in l.items():
    #         k = income_obj
    #         v = fund_obj
    #
    # print (dict_of_incomes_funds)
    # incomes_by_dates = IncomeCategories.objects.filter(owner_id=user_id,
    #                                                    income_history__date__range=(
    #                                                    content['start'], content['end']))
    # list_of_incomes_by_dates = []
    # list_of_funds_by_dates = []
    # for income in incomes_by_dates:
    #     list_of_incomes_by_dates.append(income.id)
    # print(list_of_incomes_by_dates)
    #
    # funds_by_dates = FundCategories.objects.filter(owner_id=user_id,
    #                                                income_history__income_id__in=
    #                                                list_of_incomes_by_dates)
    # for fund in funds_by_dates:
    #     list_of_funds_by_dates.append(fund.name)
    # print(list_of_funds_by_dates)

    return JsonResponse(incomes_funds_ids, safe=False, status=200)
