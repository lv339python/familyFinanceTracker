from django.urls import path, include
from .views import register_spending

urlpatterns = [
    path('register_spending/', register_spending)

]
