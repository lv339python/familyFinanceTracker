from django.urls import path, include, re_path
from .views import show_fund,show_goal_data
urlpatterns = [
    re_path(r'^$', show_fund),
    path('show_goal_data/', show_goal_data)
]
