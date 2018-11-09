"""
This module provides functions for handling Auth view.
"""
import json
import random
import string

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.views.decorators.http import require_http_methods
from requests_oauthlib import OAuth2Session

from ibudget.settings import CLIENT_SECRET, CLIENT_ID, AUTHORIZATION_BASE_URL, \
    LOCAL_URL, SCOPE, REDIRECT_URL, TOKEN_URL
from utils.jwttoken import create_token, handle_token
from utils.password_reseting import send_password_update_letter, send_successful_update_letter
from utils.validators import login_validate, is_valid_registration_data, updating_email_validate, \
    updating_password_validate
from .models import UserProfile

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
    if not login_validate(data):
        return HttpResponse('received data is not valid', status=400)
    email = data['email'].strip().lower()
    user = authenticate(email=email, password=data['password'])
    if user and user.is_active:
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
                                                 "offline", prompt="select_account")[0]
    if authorization_url:
        return JsonResponse({'url': authorization_url}, status=200)
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
        user_profile = UserProfile.get_by_email(user_data['email'])
        if user_profile:
            login(request, user_profile)
            return redirect("/#/home/")
        user = UserProfile()
        user.email = user_data['email']
        user.first_name = user_data['given_name']
        user.last_name = user_data['family_name']
        chars_pass = string.ascii_letters + string.digits + string.punctuation
        user.password = ''.join(random.choice(chars_pass) for _ in range(8))
        user.save()
        login(request, user)
        return redirect("/#/home/")
    return HttpResponse(status=400)


@require_http_methods(['GET'])
def get_profile(request):
    """
       Retrieving user profile. Handles post and get requests.
       :param request: request from the website
       :return: status 200 and dictionary with user's data if user exists,
       status 400 if user doesn't exist
    """
    user = request.user
    if user:
        return JsonResponse(user.to_dict(), status=200, safe=False)
    return JsonResponse({}, status=400)


@require_http_methods(["POST"])
def forgot_password(request):
    """
    :param request: Handles method POST
    :return: HttpResponse 400 if its bad request and HttpResponse 200 if everything is alright
    """
    data = json.loads(request.body)
    if updating_email_validate(data, 'email'):
        email = data.get('email')

    user = UserProfile.get_by_email(email=email)

    if user:
        arg = {'user_id': user.id}
        token = create_token(data=arg, expiration_time=TTL_SEND_PASSWORD_TOKEN)
        user.update(one_time_token=token)
        send_password_update_letter(user, token)
        return HttpResponse(status=200)

    return HttpResponse(status=400)


@require_http_methods(["PUT"])
def update_password(request, token=None):
    """
    :param request: Handle method PUT,
    :param token:status 200 if user successfully updated his password,
    status 400  if token fetching was unsuccessful, status 498 if invalid token,
    status 404 if user does not exist in database
    """
    identifier = handle_token(token)
    if not identifier:
        return HttpResponse(status=498)
    user = UserProfile.get_by_id(identifier['user_id'])
    if not user:
        return HttpResponse(status=404)
    if user.one_time_token == '':
        return HttpResponse(status=400)
    data = json.loads(request.body)
    if not token:
        return HttpResponse(status=400)
    if updating_password_validate(data, 'new_password'):
        new_password = data.get('new_password')
        if not user.check_password(new_password) and user.one_time_token == str(token):
            user.update(password=new_password,
                        one_time_token="")
            send_successful_update_letter(user)
            return HttpResponse(status=200)
    return HttpResponse(status=400)


@require_http_methods(["DELETE"])
def delete_user(request):
    """Handling request for delete user.
        Args:
            request (HttpRequest):request from the web page with a json containing changes to be applied.
        Returns:
            HttpResponse object.
    """
    user = request.user
    if not user:
        return HttpResponse(status=400)
    user.update(is_active=False)
    return HttpResponse(f"{user.first_name}{user.last_name} you've just deleted your account ", status=200)
