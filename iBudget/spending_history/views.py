"""
This module provides functions for handling spending_history view.
"""
import json
from decimal import Decimal

from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from utils.validators import input_spending_registration_validate

from .models import SpendingCategories, SpendingHistory, FundCategories


@require_http_methods(["POST"])
def register_spending(request):
    """Handling request for creating of spending categories list.
        Args:
            request (HttpRequest): request from server which contain
            fund, category, sum, date, comment
        Returns:
            HttpResponse status.
    """
    data = json.loads(request.body)
    if input_spending_registration_validate(data):
        return HttpResponse(status=400)

    owner = request.user
    spending = SpendingCategories.get_by_id(int(data["category"]))
    if spending.owner == owner:
        spending_history = SpendingHistory()
        spending_history.fund = FundCategories.get_by_id(int(data["type_of_pay"]))
        spending_history.spending_categories = spending
        spending_history.date = data["date"]
        spending_history.value = Decimal(data["value"])
        spending_history.owner = owner
        spending_history.comment = data["comment"]
        try:
            spending_history.save()
            return HttpResponse(status=201)
        except(ValueError, AttributeError):
            return HttpResponse(status=406)
    return HttpResponse(status=403)
