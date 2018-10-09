import json
from decimal import Decimal

from django.http import HttpResponse
from django.views.decorators.http import require_http_methods

from .models import SpendingCategories, SpendingHistory, FundCategories, UserProfile
from utils.validators import input_spending_registration_validate

@require_http_methods(["POST"])
def register_spending(request):
    data = json.loads(request.body)
    if not input_spending_registration_validate(data):
        return HttpResponse(status=400)
    #owner = request.user
    owner = UserProfile.get_by_id(5)
    categories = FundCategories.get_by_id(int(data["type_of_pay"]))
    spending = SpendingCategories.get_by_id(int(data["category"]))

    if spending.owner == owner:
        SpendingHistory.create(categories, spending, owner, Decimal(data["sum"]), data["date"], data["comment"])
        return HttpResponse(status=201)
    return HttpResponse(status=403)
