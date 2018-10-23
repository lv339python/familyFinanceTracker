from django.urls import re_path, path

from .views import (show_income_ind,
                    show_income_group)

urlpatterns = [
    re_path(r'^$', show_income_ind),
    path('show_income_group/', show_income_group),
]
