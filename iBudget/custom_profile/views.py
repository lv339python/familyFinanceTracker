
"""
CustomProfile view module
=========================
The module that provides basic logic for creating personal details and
show custom user data of profile's model objects.
"""
import json
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from utils.transaction import save_personal_info
from utils.validators import input_personal_details_validate
from .models import CustomProfile


@require_http_methods(["POST"])
def create_personal_details(request):
    """Handling request for create personal details.
    Args:
        request (HttpRequest): request from server which contain
            first name, last name, hobby, photo, birthday, user
    Returns:
        HttpResponse object.
    """
    data = json.loads(request.body)
    if not input_personal_details_validate(data):
        return HttpResponse(status=400)
    user = request.user

    if save_personal_info(
        user=user,
        first_name=data["first_name"],
        last_name=data["last_name"],
        bio=data['bio'],
        hobby=data["hobby"],
        icon=data["icon"],
        birthday=data["birthday"]):
        return HttpResponse(status=201)
    return HttpResponse(status=400)


@require_http_methods(["GET"])
def show_custom_user_data(request):
    """

    :param request: request from server which ask list of users.
    :return:HttpResponse object
    """
    user = request.user
    if user:
        users_custom_data = []
        item = CustomProfile.get_by_user(user=user)
        users_custom_data.append({'bio': item.bio,
                                  'hobby': item.hobby,
                                  'birthday': item.birthday})
        return JsonResponse(users_custom_data, status=200, safe=False)
    return JsonResponse({}, status=400)
