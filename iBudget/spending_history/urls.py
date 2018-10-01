from django.urls import path, re_path
from .views import register_spending

urlpatterns = [

    path('register_spending/', register_spending),
    # re_path(r'^$', register_spending),

]
