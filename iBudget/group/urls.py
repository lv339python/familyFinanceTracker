from django.urls import path, include
from .views import get_by_group, groups_balance, show_users_group
from django.urls import re_path


urlpatterns = [
    path('get_by_group/', get_by_group),
    path('show_users_group/', show_users_group),
    re_path(r'^$', groups_balance)
]
