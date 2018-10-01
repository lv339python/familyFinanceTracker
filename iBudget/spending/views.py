import json
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from authentication.models import UserProfile
from group.models import Group, UsersInGroups, SharedSpendingCategories
from .models import SpendingCategories

# @require_http_methods(["POST"])
# def set_shared_create(request):
#
#   data=json.loads(request.body)
#   is_shared = bool(data["is_shared"])
#   name = data["name"]
#   icon = data["icon"]
#   owner = data["owner"]
#   # owner = UserProfile.get_by_id(owner)
#   category=SpendingCategories.get_category(request, name=name)
#   if  not category:
#     SpendingCategories.create(name, icon, owner, is_shared)
#     return JsonResponse(status=201)
#   return JsonResponse("This category is alredy use", status=400)
#
# @require_http_methods(["PUT"])
# def set_shared_update(request):
#
#     data = json.loads(request.body)
#     is_shared = bool(data["is_shared"])
#     name = data["name"]
#     icon = data["icon"]
#     owner = data["owner"]
#     owner = UserProfile.get_by_id(owner)
#     category = SpendingCategories.get_category(request, name=name)
#     if category:
#       SpendingCategories.update(name, icon, owner, is_shared)
#       return JsonResponse(status=201, safe=False)
#     return JsonResponse("This category is alredy use", status=400)

@require_http_methods(["GET"])
def show_spending_ind(request):
    """Handling request for creating of spending categories list.
        Args:
            request (HttpRequest): Limitation data.
        Returns:
            HttpResponse object.
    """

    # if request.method == "GET":
    #     user = request.user
    #     if user:
    #         user_categories = []
    #         for entry in SpendingCategories.objects.filter(owner=user):
    #             user_categories.append({'id': entry.id, 'name': entry.name})
    #         return JsonResponse(user_categories, status=200, safe=False)
    # return JsonResponse({}, status=400)


    print('/n/n/n'+'/'*150)
    print(request.get_full_path())
    print('/n/n/n'+'/'*150)
    data = json.loads(request.content_params)
    print(data)

    group = data["group"]
    group = Group.get_by_id(group)

    if group:
      group_category = []
      for entry in SpendingCategories.objects.filter(id=SharedSpendingCategories.get_spend_by_group(group).id):
        group_category.append({'id': entry.id, 'name': entry.name})

        print(group_category)
      return JsonResponse(group_category, status=200, safe=False)

def show_spending(request):
    if request.method == "GET":
        user = request.user
        if user:
            user_categories = []
            for entry in SpendingCategories.objects.filter(owner=user, is_shared=True):
                user_categories.append({'id': entry.id, 'name': entry.name})
            return JsonResponse(user_categories, status=200, safe=False)
    return JsonResponse({}, status=400)


