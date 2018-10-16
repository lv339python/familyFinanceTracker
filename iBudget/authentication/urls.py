from django.urls import path
from .views import login_user, logout_user, registration, google_sign_in, google_auth_grant, forgot_password

urlpatterns = [
    path('registration/', registration),
    path('login/', login_user, name="login_user"),
    path('logout/', logout_user, name="logout_user"),
    path('auth/', google_auth_grant, name="google_auth_grant"),
    path('sign_in/', google_sign_in, name="google_sign_in"),
    path('forgot_password/', forgot_password)
]
