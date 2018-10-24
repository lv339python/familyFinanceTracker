from django.urls import path
from .views import register_spending, create_spending_history, get_month_spending

urlpatterns = [
    path('register_spending/', register_spending),
    path('show/', get_month_spending),
    path('create/', create_spending_history)
]
