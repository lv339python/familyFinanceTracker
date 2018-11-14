from django.conf.urls import url
from django.urls import path
from .views import create_personal_details, show_custom_user_data
urlpatterns = [
    path('create_personal_details/', create_personal_details),
    path('show_custom_user_data/', show_custom_user_data)
    ]
