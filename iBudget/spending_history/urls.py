from django.urls import path

from .views import register_spending, create_spending_history, get_month_spending, \
    get_spending_chart, delete_spending_history

urlpatterns = [
    path('register_spending/', register_spending),
    path('show/', get_month_spending),
    path('create/', create_spending_history),
    path('chart_spending/', get_spending_chart),
    path('delete_spending_history/<str:spending_history_id>', delete_spending_history)

]
