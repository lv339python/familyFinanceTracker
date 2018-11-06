from django.urls import path, include
from .views import register_income
from .views import track, show_total, create_xlsx

urlpatterns = [
    path('register_income/', register_income),
    path('track/', track),
    path('get_cur_incomes/', show_total),
    path('download_file/', create_xlsx),
]
