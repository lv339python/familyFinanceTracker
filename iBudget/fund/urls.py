from django.urls import path, include, re_path
from .views import show_fund, create_new_fund
urlpatterns = [
    re_path(r'^$', show_fund),
    path('create_new_fund/', create_new_fund)
]
