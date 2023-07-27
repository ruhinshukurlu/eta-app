"""
API views
"""
from django.contrib.auth import authenticate, get_user_model
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from apps.todo.models import Expectation

from .serializers import (ExpectationCreateSerializer, ExpectationListSerializer, ExpectationUpdateSerializer,
                          LoginSerializer, UserCreateSerializer)

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    """User register view, to create new account in the system"""

    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = (AllowAny,)


class LoginView(generics.GenericAPIView):
    """User login view to generate token based on username and password"""

    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)  # check if there is such a user or not
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key, "username": username})
        return Response({"error": "User not found with these credentials!"}, status=404)


class CreateExpectationView(generics.CreateAPIView):
    queryset = Expectation.objects.all()
    serializer_class = ExpectationCreateSerializer
    permission_classes = (IsAuthenticated,)


class UpdateExpectationView(generics.UpdateAPIView):
    """UpdateExpectationView view is used to extend eta and close eta"""

    queryset = Expectation.objects.all()
    serializer_class = ExpectationUpdateSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "pk"


class UserExpectationListView(generics.ListAPIView):
    """UserExpectationListView is used to get all ETAs for the looged in user"""

    queryset = Expectation.objects.all()
    serializer_class = ExpectationListSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """filter to get expectations for the logged in user"""
        expectations = super().get_queryset()
        current_user = self.request.user
        return expectations.filter(user=current_user).order_by("-id")[:10][::-1]  # returns last 10 etas for the user


class ActiveExpectationsListView(generics.ListAPIView):
    """ActiveExpectationsListView is used to get all active ETAs in the system"""

    queryset = Expectation.objects.all()
    serializer_class = ExpectationListSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        """filter to get all active expectations(ETAs) in the system ( done_at=None )"""
        expectations = super().get_queryset()
        return expectations.filter(done_at=None)
