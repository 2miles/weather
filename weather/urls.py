# pages/urls.py
from django.urls import path, include

from .views import home_page_view, detail_view

urlpatterns = [
    path("", home_page_view, name="home"),
    path("weather/<int:id>/", detail_view, name="detail"),
]
