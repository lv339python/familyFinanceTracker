from django.urls import path, include
from .views import test_track

urlpatterns = [
    path('track/', test_track)

]
