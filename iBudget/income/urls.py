from django.urls import path
from income.views import create_category

urlpatterns = [
    path('create_category/', create_category)
]
