"""
This module provides functions for handling fund view.
"""
import json

from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from group.models import SharedFunds, Group
from .models import FundCategories

@require_http_methods(["GET"])
def show_fund(request):
    """Handling request for creating of spending categories list.

        Args:
            request (HttpRequest): request from server which ask some data.
        Returns:
            HttpResponse object.
    """
    user = request.user
    if user:
        user_funds = []
        for entry in FundCategories.filter_by_user(user):
            user_funds.append({'id': entry.id, 'name': entry.name})
        return JsonResponse(user_funds, status=200, safe=False)
    return JsonResponse({}, status=400)


@require_http_methods(["POST"])
def create_new_fund(request):
    """Handling request for creating of new fund category.
    Args:
        request (HttpRequest): request from server which contain
            shred_group, name, icon
    Returns:
        HttpResponse object.
    """
    is_shared = False
    data = json.loads(request.body)
    user = request.user
    shared_group = Group.get_group_by_id(data["shared_group"])
    if shared_group:
        is_shared = True
    name = data["name"]
    icon = data["icon"]

    new_fund = FundCategories(
        name=name,
        icon=icon,
        is_shared=is_shared,
        owner=user
    )
    try:
        new_fund.save()
    except(ValueError, AttributeError):
        return HttpResponse(status=406)
    if is_shared:
        shared_fund = SharedFunds(group=shared_group,
                                  fund=new_fund)
        try:
            shared_fund.save()
        except(ValueError, AttributeError):
            return HttpResponse(status=406)
    return HttpResponse(status=201)
