from datetime import datetime

from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.todo.models import Expectation, Project

User = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create(username=validated_data["username"], email=validated_data["email"])

        user.set_password(validated_data["password"])
        user.save()

        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username"]


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password"]


class ExpectationCreateSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Expectation
        fields = ["id", "issue", "project_name", "expected_at"]

    def validate(self, attrs):
        """Validations for creating Expectation"""

        # first validation to prevent expected time is not less than current time
        current_time = datetime.now()
        date_string = str(attrs["expected_at"])[:16]  # getting string value to convert python datetime object
        input_format = "%Y-%m-%d %H:%M"
        expected_at = datetime.strptime(date_string, input_format)  # convert expected date string to python date object

        if expected_at < current_time:
            raise serializers.ValidationError({"expected_at": "Expected time cannot be less than now!"})

        # second validation to check if there user has open ETA or not
        current_user = self.context["request"].user
        current_user_open_etas = Expectation.objects.filter(user=current_user, done_at=None)

        if current_user_open_etas:
            raise serializers.ValidationError(
                {"error": "User can have only one open ETA! If you want to open new ETA please close current one."}
            )
        return attrs

    def create(self, validated_data):
        project = Project.objects.get_or_create(name=validated_data["project_name"])[0]
        validated_data.pop("project_name")
        current_user = self.context["request"].user

        expectation = Expectation.objects.create(
            user=current_user,
            project=project,
            issue=validated_data["issue"],
            expected_at=validated_data["expected_at"],
        )
        expectation.save()

        return expectation


class ExpectationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expectation
        fields = ["id", "expected_at", "done_at"]


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["name"]


class ExpectationListSerializer(serializers.ModelSerializer):
    project = ProjectSerializer()
    user = UserSerializer()

    class Meta:
        model = Expectation
        fields = [
            "id",
            "user",
            "project",
            "issue",
            "created_at",
            "expected_at",
            "done_at",
        ]
