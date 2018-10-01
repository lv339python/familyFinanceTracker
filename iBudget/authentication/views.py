"""
This module provides functions for handling Auth view.
"""

import json

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods

from utils.validators import login_validate, is_valid_registration_data
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
    # if not is_valid_registration_data(data):
    #     return HttpResponse(status=400)
    if UserProfile.get_by_email(data.get("email")):
        return HttpResponse(status=409)
    user = UserProfile()
    user.email = data.get("email")
    user.set_password(data.get("password"))
    user.save()
    return HttpResponse(status=201)


@require_http_methods(["POST"])
def login_user(request):
    """
    Login of the existing user.
    :return: status 200 if login was successful, status 400 if unsuccessful
    """


    data =json.loads(request.body.decode("utf-8"))
    # if not login_validate(data):
    #     return HttpResponse('received data is not valid', status=400)
    email = data['email'].strip().lower()
    user = authenticate(email=email, password=data['password'])
    if user is not None:
        login(request, user)
        response = HttpResponse('operation was successful provided', status=200)
        return response
    return HttpResponse('email or password is not valid', status=400)


@require_http_methods(["GET"])
def logout_user(request):
    """
    Logout of the existing user. Handles post and get requests.
    :param request: request from the website
    :return: status 200
    """


    logout(request)
    response = HttpResponse('operation was successful provided', status=200)
    return response


