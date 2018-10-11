from django.urls import path, include
from .views import register_spending\
    # , register_spending_group
urlpatterns = [
    path('register_spending/', register_spending),
    # path('register_spending_group/', register_spending_group)
]
