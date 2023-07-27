"""
API urls
"""
from django.urls import path

from .views import (ActiveExpectationsListView, CreateExpectationView, LoginView, RegisterView, UpdateExpectationView,
                    UserExpectationListView)

app_name = "todo"

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("create-expectation/", CreateExpectationView.as_view(), name="create-expectation"),
    path("update-expectation/<int:pk>/", UpdateExpectationView.as_view(), name="update-expectation"),
    path("user-expectations/", UserExpectationListView.as_view(), name="user-expectations"),
    path("active-expectations/", ActiveExpectationsListView.as_view(), name="active-expectations"),
]
