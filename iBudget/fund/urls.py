from django.urls import path, include, re_path
from .views import show_spending_ind, register_financial_goal_group, show_fund_group
urlpatterns = [
    re_path(r'^$', show_spending_ind),
    path('register_financial_goal_group/', register_financial_goal_group),
    path('show_fund_group/', show_fund_group)
]
