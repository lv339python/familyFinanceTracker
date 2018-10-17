from django.urls import path, include
from .views import get_by_group

urlpatterns = [

    path('get_by_group/', get_by_group)

]
