"""
This module provides functions for handling Auth view.
"""

import json

from django.http import HttpResponse
from django.views.decorators.http import require_http_methods

from utils.validators import is_valid_registration_data
from .models import UserProfile


@require_http_methods(["POST"])
def registration(request):
    """Handling request for create new UserProfile

        Args:
            request (HttpRequest): client data
        Returns:
            HttpResponse object.
    """

    data = json.loads(request.body)
    if not is_valid_registration_data(data):
        return HttpResponse(status=400)
    if UserProfile.get_by_email(data.get("email")):
        return HttpResponse(status=409)
    user = UserProfile()
    user.email = data.get("email")
    user.set_password(data.get("password"))
    user.save()
    return HttpResponse(status=201)
