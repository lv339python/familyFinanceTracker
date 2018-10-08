from django.urls import re_path

from spending.views import set_spending_limitation_ind, show_spending_ind

from .views import show_spending_ind, show_spending
# set_shared_update, set_shared_create
#
#
urlpatterns = [
  re_path(r'^$', show_spending_ind),
  re_path(r'^set_limit/', set_spending_limitation_ind),
#
    # path('set_shared_create/', set_shared_create),
    # path('set_shared_update/', set_shared_update),
    path('show_spending_ind/', show_spending_ind),
    re_path(r'^$',show_spending)
]
