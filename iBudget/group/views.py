from django.http import JsonResponse, HttpResponse
from .models import Group, SharedSpendingCategories, SpendingCategories
from django.views.decorators.http import require_http_methods
import json

from authentication.models import UserProfile

@require_http_methods(["GET"])
def get_by_group(request):
    """
     :param request:
     :return:status 200
    """



    user = request.user
    if user:
      user_groups = []
      for entry in Group.objects.filter(owner=user):
          user_groups.append({'id': entry.id, 'name': entry.name})
      return JsonResponse(user_groups, status=200, safe=False)










# @require_http_methods(["GET"])
# def get_by_group(request):
#   """
#   :param request:
#   :return:status 200
#   """
#
#   group_spend={
#     # "group": [],
#     "spending_categories": []
#
#   }
#
#   data=json.loads(request.body)
#
#
#   all_categories_in_groups=SharedSpendingCategories.objects.all()
#   # for groups in all_categories_in_groups:
#   #   group_spend['group'].append(groups.group)
#   for groups in all_categories_in_groups:
#     group_spend['spending_categories'].append(groups.spending_categories)
#
  # group_spend["group"]=[SharedSpendingCategories.get_spend_by_group(group).group for group in group_spend["group"]]
  # group_spend["spending_categories"]=[SharedSpendingCategories.get_spendinng_category(spending_categories).
        # spending_categories for spending_categories in group_spend["spending_categories"]
#         if SharedSpendingCategories.get_spendinng_category(spending_categories).id == SharedSpendingCategories.
#         get_spend_by_group(data["group"]).group.id]
#   print (group_spend)
#   return group_spend




