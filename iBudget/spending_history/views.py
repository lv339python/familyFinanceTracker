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
    # if input_spending_registration_validate(data):
    #     return HttpResponse(status=400)
    owner = request.user
    fund = FundCategories.get_by_id(int(data["type_of_pay"]))
    print(data.keys())
    print(data['category'])
    spending = SpendingCategories.get_by_id(int(data["category"]))
    if spending.owner == owner:
        SpendingHistory.create(fund,
                               spending,
                               owner,
                               Decimal(data["sum"]),
                               data["date"],
                               data["comment"])
        return HttpResponse(status=201)
    return HttpResponse(status=403)

# @require_http_methods(["POST"])
# def register_spending_group(request):
#     """Handling request for creating of spending categories list for group.
#         Args:
#             request (HttpRequest): request from server which contain
#             fund, shared_category, sum, date, comment
#         Returns:
#             HttpResponse status.
#     """
#     data = json.loads(request.body)
#     # if input_spending_registration_validate(data):
#     #     return HttpResponse(status=400)
#     owner = request.user
#     fund = FundCategories.get_by_id(int(data["type_of_pay"]))
#     spending = SpendingCategories.get_by_id(int(data["shared_category"]))
#     if spending.groups.isinstanse.owner == owner:
#         SpendingHistory.create(fund,
#                                spending,
#                                owner,
#                                Decimal(data["sum"]),
#                                data["date"],
#                                data["comment"])
#         return HttpResponse(status=201)
#     return HttpResponse(status=403)
