from django.urls import path
from .views import register_spending, create_spending_history

urlpatterns = [
    path('register_spending/', register_spending),
    path('show/', create_spending_history)
]
