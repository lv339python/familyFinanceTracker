from django.conf.urls import url
from django.urls import path
from .views import (login_user,
                    logout_user,
                    registration,
                    google_sign_in,
                    google_auth_grant,
                    get_profile,
                    forgot_password,
                    update_password,
                    delete_user)

urlpatterns = [
    path('registration/', registration),
    path('login/', login_user, name="login_user"),
    path('logout/', logout_user, name="logout_user"),
    path('auth/', google_auth_grant, name="google_auth_grant"),
    path('sign_in/', google_sign_in, name="google_sign_in"),
    path('profile/', get_profile, name="get_profile"),
    path('forgot_password/', forgot_password),
    path('delete_user/', delete_user),
    url(r'^update_password/(?P<token>.+)$', update_password, name="update_password")
    ]
