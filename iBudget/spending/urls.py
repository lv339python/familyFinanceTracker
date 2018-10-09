from django.urls import re_path, path
from .views import  show_spending_ind, set_spending_limitation_ind, show_spending_group
    #
# set_shared_update, set_shared_create show_spending_ind,


urlpatterns = [
  # re_path(r'^$', show_spending_ind),
  # path('set_shared_create/', set_shared_create),
  # path('set_shared_update/', set_shared_update),
  # path('<group_id>', show_spending_ind),
  path('show_spending_ind/', show_spending_ind),
  re_path(r'^set_limit/', set_spending_limitation_ind),
  path('show_spending_group/', show_spending_group)
]
