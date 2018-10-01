from django.urls import re_path

from spending.views import set_spending_limitation_ind, show_spending_ind

urlpatterns = [
  re_path(r'^user/(?P<user_id>\d+)/$', show_spending_ind),
  re_path(r'^user/(?P<user_id>\d+)/set_limit/(?P<spending_id>\d+)', set_spending_limitation_ind),
]
