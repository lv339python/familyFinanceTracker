from django.urls import re_path, path
from .views import  show_spending_ind, set_spending_limitation_ind, show_spending_group



urlpatterns = [
  re_path(r'^$', show_spending_ind),
  re_path(r'^set_limit/', set_spending_limitation_ind),
  path('show_spending_group/', show_spending_group)
]
