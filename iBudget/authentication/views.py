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

from utils.validators import login_validate, is_valid_registration_data, is_valid_password,\
    updating_email_validate, updating_password_validate
from ibudget.settings import CLIENT_SECRET, CLIENT_ID, AUTHORIZATION_BASE_URL, \
  LOCAL_URL, SCOPE, REDIRECT_URL, TOKEN_URL
from .models import UserProfile
from utils.jwttoken import create_token, handle_token
from utils.password_reseting import send_password_update_letter, send_successful_update_letter

TTL_SEND_PASSWORD_TOKEN = 60 * 60
USER_TTL_NOTIFICATOR = TTL_SEND_PASSWORD_TOKEN / 60
TTL_USER_ID_COOKIE = 60 * 60 * 24 * 14


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


@require_http_methods(["POST"])
def send_email(request):
    """

    :param request: method POST
    :return: HttpResponse 400 if its bad request and HttpResponse 200 if everything is alright
    """
    data = json.loads(request.body)
    if updating_email_validate(data, 'email'):
        email = data.get('email')

    user = UserProfile.get_by_email(email=email)
    if user:
        arg = {'user_id': user.id}
        token = create_token(data=arg, expiration_time=TTL_SEND_PASSWORD_TOKEN)
        send_password_update_letter(user, token)
        return HttpResponse(status=200)
    return HttpResponse(status=400)


@require_http_methods(["POST"])
def update_password(request, token=None):
    """Handles POST request."""
    if not token:
        return HttpResponse(status=400)
    identifier = handle_token(token)
    if not identifier:
        return HttpResponse(status=498)
    user = UserProfile.get_by_id(identifier['user_id'])
    if not user:
        return HttpResponse(status=404)
    data = request.body
    if updating_password_validate(data, 'new_password'):
        new_password = data.get('new_password')
        if not user.check_password(new_password):
            user.update(password=new_password)
            send_successful_update_letter(user)
            return HttpResponse(status=200)
        return HttpResponse(status=400)
    return HttpResponse(status=400)


@require_http_methods(["POST"])
def change_password(request):
    """Change_password UserProfile"""
    user = request.user
    data = json.loads(request.body)
    if user.check_password(data['OldPassword']):
        if is_valid_password(data['NewPassword']):
            user.update(password=data['NewPassword'])
            return HttpResponse(status=200)
        return HttpResponse(status=400)
    return HttpResponse(status=400)
