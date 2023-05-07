from datetime import datetime

from django.db.models import Q
from django.http import Http404
from rest_framework import generics, permissions, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Task, User
from .permissions import IsOwnerOrAdmin
from .serializers import TaskSerializer, UpdateProfileSerializer, UserSerializer


def get_user(pk):
    try:
        return User.objects.get(pk=pk)
    except User.DoesNotExist as err:
        raise Http404 from err


class ListUsers(APIView):
    """
    Create a new user and list all of them.
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

        args = ()
        kwargs = {}

        # field filtering
        if "name" in request.query_params:
            kwargs["name__icontains"] = request.query_params["name"]
        if "email" in request.query_params:
            kwargs["email__icontains"] = request.query_params["email"]

        # search filtering
        if "search" in request.query_params:
            search = request.query_params["search"]
            args = Q(name__icontains=search) | Q(email__icontains=search)

        # pagination
        paginator = PageNumberPagination()
        paginator.page_size = 2
        queryset = User.objects.filter(*args, **kwargs).order_by("-updated_at")
        result_page = paginator.paginate_queryset(queryset, request)

        serializer = UserSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


listUsersAPIView = ListUsers.as_view()


class UserProfile(generics.GenericAPIView):
    """
    Retrieve or update a user.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

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


class TaskList(generics.ListCreateAPIView):
    """
    List all tasks, or create a new task.
    """

    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    permission_classes = [permissions.IsAuthenticated]

    filterset_fields = ["title", "description", "owner__name", "owner__email", "effort"]
    search_fields = ["title", "owner__name", "owner__email"]
    ordering_fields = "__all__"

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Task.objects.all()
        return Task.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


taskListAPIView = TaskList.as_view()


class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a task instance.
    """

    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]


taskDetailAPIView = TaskDetail.as_view()


class TaskCompleting(generics.UpdateAPIView):
    """
    Complete a task.
    """

    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]
    allowed_methods = ["PATCH"]

    def update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        request.data.clear()
        request.data["completed_at"] = datetime.now()
        return super().update(request, *args, **kwargs)


taskCompletingAPIView = TaskCompleting.as_view()
