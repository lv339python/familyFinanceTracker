from django.urls import re_path, path

from spending.views import (set_spending_limitation_ind,
                            show_spending_ind,
                            group_limit,
                            set_group_limit,
                            change_group_limit,
                            create_spending_category)

urlpatterns = [
    re_path(r'^$', show_spending_ind),
    re_path(r'^set_limit/', set_spending_limitation_ind),
    path('admin/limit/', group_limit),
    path('admin/set_limit/', set_group_limit),
    path('admin/change_limit/<str:category_name>', change_group_limit),
    re_path(r'^add/', create_spending_category)
]
