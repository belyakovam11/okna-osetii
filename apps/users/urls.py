from django.urls import path

from . import pages

urlpatterns = [
    path("register/", pages.register, name="user_register"),
    path("login/", pages.user_login, name="user_login"),
    path("logout/", pages.user_logout, name="user_logout"),
    path("profile/", pages.user_profile, name="user_profile"),
]
