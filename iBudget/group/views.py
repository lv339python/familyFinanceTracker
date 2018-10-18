"""
This module provides functions for handling group view.
"""
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Group, UsersInGroups


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


@require_http_methods(["GET"])
def show_users_group(request):
    """Handling request for creating of user's groups list.
    Args:
        request (HttpRequest): request from server which ask list of groups for user.
    Returns:
        HttpResponse object.
    """
    user = request.user
    if user:
        groups = []
        for item in UsersInGroups.filter_by_user(user):
            groups.append({'name': item.group.name, 'id': item.group.id})
        return JsonResponse(groups, status=200, safe=False)
    return JsonResponse({}, status=400)
