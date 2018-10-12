from django.urls import re_path
from .views import groups_balance

urlpatterns = [
re_path(r'^$', groups_balance),
]
