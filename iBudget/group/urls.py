from django.urls import path

from .views import get_by_group
  # , show_shared_category

urlpatterns = [

    path('get_by_group/', get_by_group),
    # path('show_shared_category/', show_shared_category),


]
