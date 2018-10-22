from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
import json
from .models import IncomeCategories, FundCategories, IncomeHistory


@require_http_methods(['POST'])
def test_track(request):
    content = request.body
    content = json.loads(content)
    user_id = request.user
    if len(content) <= 1:
        return HttpResponse('You did not choose any dates or you chose only one date out of two',
                            status=400)
    incomes_funds = IncomeHistory.objects.filter(date__date__range=(content['start'], content['end']))
    l = [{i.income_id: i.fund_id for i in incomes_funds}]
    print(l)
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

    return JsonResponse(content, status=200)
