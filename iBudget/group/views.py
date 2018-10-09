from django.http import JsonResponse
from .models import Group
from django.views.decorators.http import require_http_methods


@require_http_methods(["GET"])
def get_by_group(request):
    """Handling request for creating of group list.
        Args:
            request (HttpRequest): request from server which ask some data.
        Returns:
            HttpResponse object.
    """

    user = request.user
    if user:
      user_groups = []
      for entry in Group.group_filter_by_owner_id(user):
          user_groups.append({'id': entry.id, 'name': entry.name})
      return JsonResponse(user_groups, status=200, safe=False)
    return JsonResponse({}, status=400)










