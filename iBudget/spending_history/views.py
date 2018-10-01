import json
from django.http import HttpResponse
from .models import SpendingHistory
from fund.models import FundCategories
from spending.models import SpendingCategories
from django.views.decorators.http import require_http_methods
from group.models import Group,SharedSpendingCategories



@require_http_methods(['POST'])
def register_spending(request):
    data = json.loads(request.body)
    owner = request.user
    fund_id = int(data["card"])

    spending_id = int(data["category"])
    #   category-називаємо на бекуб потім так само називаємо на фронті
    spending = SpendingCategories.get_by_spend_id(spending_id)
    # spending_id-можна написати любу змінну

    sum = int(data["sum"])
    comment = data["comment"]
    date = data.get("date")
    categories = FundCategories.get_by_fund_id(fund_id)




    # if spending.owner == owner:
    #   SpendingHistory.create(categories, spending, date, sum, owner, comment)
    #   return HttpResponse(status=201)

    if spending.groups.instance.owner == owner:
      # groups-список груп до яких налкжить даний користувач
      SpendingHistory.create(categories, spending, date, sum, owner, comment)
      return HttpResponse(status=201)
    return HttpResponse (status=403)





























