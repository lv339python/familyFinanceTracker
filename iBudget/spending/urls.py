from django.urls import re_path, path

from spending.views import (set_spending_limitation_ind,
                            show_spending_ind,
                            show_spending_group,
                            group_limit,
                            set_group_limit,
                            change_group_limit)

urlpatterns = [
  re_path(r'^$', show_spending_ind),
  re_path(r'^set_limit/', set_spending_limitation_ind),
  path('show_spending_group/', show_spending_group),
  path('admin/limit/', group_limit),
  path('admin/set_limit/', set_group_limit),
  path('admin/change_limit/<str:category_name>', change_group_limit)
]
