from django.urls import path
from .views import track, show_total

urlpatterns = [
    path('track/', track),
    path('get_cur_incomes/', show_total),

]
