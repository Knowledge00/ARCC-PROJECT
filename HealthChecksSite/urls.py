from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name = "healthcheck"),
    path("test/", views.test, name = "test"),
]