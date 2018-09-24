from django.urls import path

from .views import login_user, logout_user, registration

urlpatterns = [
    path('registration/', registration),
    path('login/', login_user, name="login_user"),
    path('logout/', logout_user, name="logout_user"),
]
