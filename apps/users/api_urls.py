from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("users", views.UserViewSet, basename="users")

urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="api_user_register"),
    path("login/", views.LoginView.as_view(), name="api_user_login"),
    path("profile/", views.ProfileView.as_view(), name="api_user_profile"),
    path("", include(router.urls)),
]
