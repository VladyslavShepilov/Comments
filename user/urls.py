from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.contrib.auth.views import LogoutView

from .views import UserDetailView, UserLoginView, UserRegisterView, UserUpdateView


urlpatterns = [
    path("user/register/", UserRegisterView.as_view(), name="register"),
    path("user/update/", UserUpdateView.as_view(), name="update"),
    path("user/login/", UserLoginView.as_view(), name="login"),
    path(
        "user/logout/",
        LogoutView.as_view(template_name="user/logout.html"),
        name="logout",
    ),
    path("user/<int:pk>/", UserDetailView.as_view(), name="user-detail"),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
