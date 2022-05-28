from django.urls import path, include
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
)

from .views import register_view

urlpatterns = [
    path("signup/", register_view, name="signup"),
]
