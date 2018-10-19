from django.urls import path, include, re_path
from .views import show_fund
urlpatterns = [
    re_path(r'^$', show_fund)
]
