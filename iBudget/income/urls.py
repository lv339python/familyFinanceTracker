from django.urls import re_path, path

from .views import (show_income_ind)

urlpatterns = [
    re_path(r'^$', show_income_ind),
]
