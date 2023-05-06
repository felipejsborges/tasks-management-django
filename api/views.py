from datetime import datetime

from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Task, User
from .serializers import TaskSerializer, UpdateProfileSerializer, UserSerializer


def get_task(pk):
    try:
        return Task.objects.get(pk=pk)
    except Task.DoesNotExist as err:
        raise Http404 from err


def get_user(pk):
    try:
        return User.objects.get(pk=pk)
    except User.DoesNotExist as err:
        raise Http404 from err


class UserCreate(APIView):
    """
    Register a new user.
    """

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(username=serializer.validated_data["email"])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        if not request.user.is_superuser:
            return Response(status=status.HTTP_403_FORBIDDEN)
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


userCreateAPIView = UserCreate.as_view()


class UserProfile(APIView):
    """
    Retrieve the current user.
    """

    def get(self, request):
        pk = request.user.id
        user = get_user(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request):
        pk = request.user.id
        user = get_user(pk)
        serializer = UpdateProfileSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


userProfileAPIView = UserProfile.as_view()


class TaskList(APIView):
    """
    List all tasks, or create a new task.
    """

    def get(self, request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_403_FORBIDDEN)
        tasks = (
            Task.objects.all()
            if request.user.is_superuser
            else Task.objects.filter(owner=request.user)
        )
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


taskListAPIView = TaskList.as_view()


class TaskDetail(APIView):
    """
    Retrieve, update or delete a task instance.
    """

    def get(self, request, pk):
        task = get_task(pk)
        if task.owner != request.user and not request.user.is_superuser:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    def put(self, request, pk):
        task = get_task(pk)
        if task.owner != request.user and not request.user.is_superuser:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        task = get_task(pk)
        if task.owner != request.user and not request.user.is_superuser:
            return Response(status=status.HTTP_403_FORBIDDEN)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


taskDetailAPIView = TaskDetail.as_view()


class TaskCompleting(APIView):
    """
    Complete a task.
    """

    def patch(self, request, pk):
        task = get_task(pk)
        if task.owner != request.user and not request.user.is_superuser:
            return Response(status=status.HTTP_403_FORBIDDEN)
        task.completed_at = datetime.now()
        serializer = TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


taskCompletingAPIView = TaskCompleting.as_view()
