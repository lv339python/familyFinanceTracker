"""
This module provides functions for handling Auth view.
"""

import json

from django.http import HttpResponse

from utils.validators import is_valid_registration_data
from .models import UserProfile


def registration(request):
    """Handling request for create new UserProfile

        Args:
            request (HttpRequest): client data
        Returns:
            HttpResponse object.
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        if not is_valid_registration_data(data):
            return HttpResponse(status=400)
        if UserProfile.get_by_email(data.get("email")):
            return HttpResponse(status=400)
        user = UserProfile()
        user.email = data.get("email")
        user.set_password(data.get("password"))
        user.save()
        return HttpResponse(status=201)
    return HttpResponse(status=405)
