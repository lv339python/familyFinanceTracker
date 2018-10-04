from django.urls import path


from .views import login_user, logout_user, registration, google_sign_in, google_auth_grant, change_password

urlpatterns = [
    path('registration/', registration),
    path('login/', login_user, name="login_user"),
    path('logout/', logout_user, name="logout_user"),
    path('auth/', google_auth_grant, name="google_auth_grant"),
    path('sign_in/', google_sign_in, name="google_sign_in"),
    path('change_password/', change_password, name="change_password"),
]
