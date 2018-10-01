from django.urls import re_path, include
from .views import show_fund_ind

urlpatterns = [

    re_path(r'^$', show_fund_ind)

]
