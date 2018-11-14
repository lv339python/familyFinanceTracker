from django.urls import re_path, path

from .views import (show_income_ind,
                    show_income_group,
                    create_category,
                    delete_income,
                    income_summary)
from django.urls import path


urlpatterns = [
    re_path(r'^$', show_income_ind),
    path('show_income_group/', show_income_group),
    path('create_category/', create_category),
    path('delete_income/<str:income_category_id>', delete_income),
    path('summary/', income_summary)
]
