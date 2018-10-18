from django.urls import path, include
from .views import get_by_group, show_users_group

urlpatterns = [
    path('show_users_group/', show_users_group),
    path('get_by_group/', get_by_group)
]
