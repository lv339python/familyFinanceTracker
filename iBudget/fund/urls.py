from django.urls import path, re_path

from .views import (show_fund,
                    users_shared_fund,
                    create_new_fund,
                    show_goal_data,
                    show_fund_by_group,
                    create_new_goal)

urlpatterns = [
    re_path(r'^$', show_fund),
    path('show_goal_data/', show_goal_data),
    path('users_shared_fund/', users_shared_fund),
    path('create_new_fund/', create_new_fund),
    path('show_fund_by_group/', show_fund_by_group),
    path('create_new_goal/', create_new_goal)
]
