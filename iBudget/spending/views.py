"""
This module provides functions for spending tracking.
"""
import calendar
import json
from datetime import date
from django.http import HttpResponse
from utils.validators import is_valid_spending_limitation
from .models import SpendingLimitation, SpendingCategories


def set_spending_limitation(request):
  """Handling request for create spending limitation.

      Args:
          request (HttpRequest): Limitation data.
      Returns:
          HttpResponse object.
  """
  if request.method == "POST":
    data = json.loads(request.body)

  if not is_valid_spending_limitation(data):
    return HttpResponse(status=409)
  spending_limitation = SpendingLimitation()
  if data['month']:
    spending_limitation.start_date = date(data['year'], data['month'], 1)
    spending_limitation.finish_date = date(data['year'],
                                           data['month'],
                                           (calendar.monthrange(data['year'], data['month']))[1])
  else:
    spending_limitation.start_date = date(data['year'], 1, 1)
    spending_limitation.finish_date = date(data['year'], 12, 31)

  spending_limitation.value = round(data['value'], 2)
  spending_limitation.spending_category = SpendingCategories.get_by_id(data['spending_category'])

  print(spending_limitation.value)
  # spending_limitation.save()

  return HttpResponse(status=201)
