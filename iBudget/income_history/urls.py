from django.urls import path, include
from .views import register_income, delete_income_history
from .views import track, show_total

urlpatterns = [
    path('register_income/', register_income),
    path('track/', track),
    path('get_cur_incomes/', show_total),
    path('delete_income_history/<income_history_id>', delete_income_history)

]
