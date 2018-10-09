from django.urls import re_path
from .views import show_spending_ind

urlpatterns = [

    re_path(r'^$', show_spending_ind)

]
