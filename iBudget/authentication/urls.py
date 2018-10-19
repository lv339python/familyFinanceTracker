from django.urls import path
from .views import login_user, logout_user, registration, google_sign_in, google_auth_grant, send_email, \
    update_password, change_password

urlpatterns = [
    path('registration/', registration),
    path('login/', login_user, name="login_user"),
    path('logout/', logout_user, name="logout_user"),
    path('auth/', google_auth_grant, name="google_auth_grant"),
    path('sign_in/', google_sign_in, name="google_sign_in"),
    path('send_email/', send_email),
    path('update_password/', update_password),
    path('change_password/', change_password)
]
