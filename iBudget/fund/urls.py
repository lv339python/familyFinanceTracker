from django.urls import path, include, re_path
from .views import show_fund, show_goal_data

from .views import show_fund, register_financial_goal, users_shared_fund, create_new_fund
urlpatterns = [
    re_path(r'^$', show_fund),
    path('show_goal_data/', show_goal_data),

    re_path(r'^$', show_fund),
    path('register_financial_goal/', register_financial_goal),
    path('users_shared_fund/', users_shared_fund),
    path('create_new_fund/', create_new_fund)
]
