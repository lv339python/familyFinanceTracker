import json
from decimal import Decimal

from django.http import HttpResponse
from django.views.decorators.http import require_http_methods

from utils.validators import input_income_registration_validate
from .models import IncomeCategories, IncomeHistory, FundCategories



@require_http_methods(["POST"])
def register_income(request):
    """Handling request for creating of spending categories list.
        Args:
            request (HttpRequest): request from server which contain
            fund, category, sum, date, comment
        Returns:
            HttpResponse status.
    """
    data = json.loads(request.body)
    if not input_income_registration_validate(data):
        return HttpResponse('Please, fill all required fields', status=400)

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
    except(ValueError, AttributeError):
        return HttpResponse(status=406)
    return HttpResponse('Your income was successfully registered', status=201)
