from django.urls import path, re_path

from .views import show_spending_ind, show_spending
# set_shared_update, set_shared_create
#
#
urlpatterns = [
#
    # path('set_shared_create/', set_shared_create),
    # path('set_shared_update/', set_shared_update),
    path('show_spending_ind/', show_spending_ind),
    re_path(r'^$',show_spending)
]
