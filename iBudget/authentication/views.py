"""
This module provides functions for handling Auth view.
"""

import json
from random import randint

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import redirect
from requests_oauthlib import OAuth2Session

from utils.validators import login_validate, is_valid_registration_data
from ibudget.settings import CLIENT_SECRET, CLIENT_ID, AUTHORIZATION_BASE_URL, \
  LOCAL_URL, SCOPE, REDIRECT_URL, TOKEN_URL
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
    UserProfile.create(data.get("email"), data.get("password"))
    return HttpResponse(status=201)


@require_http_methods(["POST"])
def login_user(request):
    """
    Login of the existing user.
    :return: status 200 if login was successful, status 400 if unsuccessful
    """


    data = json.loads(request.body.decode("utf-8"))
    if not login_validate(data):
        return HttpResponse('received data is not valid', status=400)
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


def google_auth_grant(request):
    """
    Receiving authorization grant after redirection to Google API
    :param request: request from the website
    :return: redirect to GoogleOauth2 API if Oauth2 session object generated successful,
    status 400 if unsuccessful
    """

    google = OAuth2Session(CLIENT_ID, scope=SCOPE, redirect_uri=REDIRECT_URL)
    authorization_url = google.authorization_url(AUTHORIZATION_BASE_URL, access_type=
                                                 "offline", prompt="select_account")
    if authorization_url:
        return redirect(authorization_url)

    return HttpResponse(status=400)


def google_sign_in(request):
    """
    Retrieving authorization token and signing up with google account info
    :param request: request from the website
    :return: status 200 if user is already in database , status 201 if user was auto-registered ,
    status 400  if token fetching was unsuccessful
    """
    google = OAuth2Session(CLIENT_ID, scope=SCOPE, redirect_uri=REDIRECT_URL)
    google.fetch_token(TOKEN_URL, client_secret=CLIENT_SECRET, authorization_response=
                       LOCAL_URL + request.get_full_path(), code=request.GET["code"])
    user_data = google.get('https://www.googleapis.com/oauth2/v1/userinfo').json()
    if user_data:
        if UserProfile.get_by_email(user_data['email']):
            login(request, UserProfile.get_by_email(user_data['email']))
            return HttpResponse('Operation was successful provided', status=200)
        user = UserProfile()
        user.email = user_data['email']
        user.first_name = user_data['given_name']
        user.last_name = user_data['family_name']
        user.password = str(randint(0, 9999))
        user.save()
        return HttpResponse(status=201)
    return HttpResponse(status=400)
