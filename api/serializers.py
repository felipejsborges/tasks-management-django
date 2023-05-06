from rest_framework import serializers

from .models import Task, User


class TaskSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = Task
        fields = [
            "id",
            "owner",
            "created_at",
            "updated_at",
            "title",
            "description",
            "effort",
            "completed_at",
        ]


class UserSerializer(serializers.ModelSerializer):
    tasks = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Task.objects.all(), required=False
    )

    class Meta:
        model = User
        fields = [
            "id",
            "tasks",
            "name",
            "password",
            "email",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
            name=validated_data["name"],
        )
        user.set_password(validated_data["password"])
        user.save()

        return user


class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "name",
            "email",
        ]
