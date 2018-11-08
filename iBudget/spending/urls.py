from django.urls import re_path, path

from spending.views import (set_spending_limitation_ind_fix,
                            show_spending_ind,
                            show_spending_group,
                            group_limit,
                            set_group_limit,
                            change_group_limit,
                            create_spending_category,
                            delete_spending_category,
                            set_limitation_period, set_spending_limitation_ind_arb)

urlpatterns = [
    re_path(r'^$', show_spending_ind),
    re_path(r'^set_limit_fix/', set_spending_limitation_ind_fix),
    re_path(r'^set_limit_arb/', set_spending_limitation_ind_arb),
    re_path(r'^set_period/', set_limitation_period),
    path('show_spending_group/', show_spending_group),
    path('admin/limit/', group_limit),
    path('admin/set_limit/', set_group_limit),
    path('admin/change_limit/<str:category_name>', change_group_limit),
    re_path(r'^add/', create_spending_category),
    path('delete_spending_category/<str:spending_id>', delete_spending_category),
]
