from django.urls import re_path

from spending.views import set_spending_limitation_ind, show_spending_ind

urlpatterns = [
  re_path(r'^$', show_spending_ind),
  re_path(r'^set_limit/', set_spending_limitation_ind),
]
