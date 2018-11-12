"""
Middleware
==========
The module that provides custom application's middlewares and and provides custom JSON check.
"""

from django.http import HttpResponse

ANONYMOUS_USERS_PATHS = ['/api/v1/authentication/login/',
                         '/api/v1/authentication/forgot_password/',
                         '/api/v1/authentication/auth/',
                         '/api/v1/authentication/sign_in/',
                         '/api/v1/authentication/registration/']
ENCODING = "utf-8"


class LoginRequiredMiddleware():#pylint: disable=too-few-public-methods
    """
    The class that represents the middleware that permits only a few available paths
    for anonymous users and provides custom JSON check.
    """

    def __init__(self, get_response):
        """Constructor method that creates middleware instance."""

        self.get_response = get_response

    def __call__(self, request):
        """
        Method that makes the middleware instance callable and implements authentication
        verification and provides custom JSON check.
        """
        if not request.path_info.startswith('/api'):
            response = self.get_response(request)
            return response

        # if request.method == 'POST' or request.method == 'PUT':
        #     try:
        #         if not request.path_info.startswith('/api/v1/files'):
        #             request._body = json.loads(request.body.decode(ENCODING))
        #     except (SyntaxError, JSONDecodeError):
        #         return HttpResponse(status=400)
        #         # dont forget about loger
        for current_path in ANONYMOUS_USERS_PATHS:
            if request.path_info.startswith(current_path):

                if request.user.is_authenticated:
                    return HttpResponse(status=400)
                response = self.get_response(request)
                return response
        if not request.user.is_authenticated:
            return HttpResponse(status=403)
        response = self.get_response(request)
        return response
