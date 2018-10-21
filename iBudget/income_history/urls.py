from django.urls import path, include
from .views import register_income
urlpatterns = [
    path('register_income/', register_income)
]
