from django.urls import path, include
from .views import get_by_group, \
    groups_balance, \
    show_users_group, \
    create_new_group, \
    show_users_group_data, \
    add_new_users_to_group

from django.urls import re_path


urlpatterns = [
    path('get_by_group/', get_by_group),
    path('show_users_group/', show_users_group),
    re_path(r'^$', groups_balance),
    path('create_new_group/', create_new_group),
    path('show_users_group_data/', show_users_group_data),
    path('add_new_users_to_group/', add_new_users_to_group)
]
