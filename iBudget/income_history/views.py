from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
import json
from .models import IncomeHistory, IncomeCategories


@require_http_methods(['POST'])
def test_track(request):
    content = request.body
    content = json.loads(content)
    user_id = request.user
    # income_inst = IncomeCategories.objects.get(owner_id=user['id'])
    # print(income_inst)
    if len(content) <= 1:
        return HttpResponse('You did not choose any dates or you chose only one date out of two',
                            status=400)
    incomes_by_dates = IncomeHistory.objects.filter(income_id__incomecategories__owner_id=user_id)
    # date__range=(content['start'], content['end'])
    print(incomes_by_dates)
    return JsonResponse(content, status=200)
