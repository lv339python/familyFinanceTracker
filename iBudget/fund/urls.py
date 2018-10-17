from django.urls import path, include, re_path
from .views import show_fund, register_financial_goal, show_fund_group
urlpatterns = [
    re_path(r'^$', show_fund),
    path('register_financial_goal/', register_financial_goal),
    path('show_fund_group/', show_fund_group)
]
