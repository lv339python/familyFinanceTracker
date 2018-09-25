from django.urls import path, include

from spending.views import set_spending_limitation

urlpatterns = [
  path('spend/', set_spending_limitation)
]
