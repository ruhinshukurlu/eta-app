"""
Template urls for the task
"""
from django.urls import path

from .views import active_etas, index, login

urlpatterns = [
    path("", index, name="index"),
    path("active-etas", active_etas, name="active-etas"),
    path("login/", login, name="login"),
    path("register/", login, name="register"),
]
