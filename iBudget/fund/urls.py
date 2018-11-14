from django.urls import path, re_path

from .views import (show_fund,
                    show_goal,
                    users_shared_fund,
                    create_new_fund,
                    show_goal_data,
                    show_fund_by_group,
                    show_goal_by_group,
                    create_new_goal,
                    get_balance,
                    delete_fund_goal_category,
                    fund_summary)

urlpatterns = [
    re_path(r'^$', show_fund),
    path('show_goal/', show_goal),
    path('show_goal_data/', show_goal_data),
    path('users_shared_fund/', users_shared_fund),
    path('create_new_fund/', create_new_fund),
    path('show_fund_by_group/', show_fund_by_group),
    path('show_goal_by_group/', show_goal_by_group),
    path('create_new_goal/', create_new_goal),
    path('get_balance/', get_balance),
    path('delete_fund_goal_category/<str:fund_id>', delete_fund_goal_category),
    path('summary/', fund_summary)
]
