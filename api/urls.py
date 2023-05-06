from django.urls import path

from . import views

urlpatterns = [
    path("tasks", views.taskListAPIView),
    path("tasks/<int:pk>", views.taskDetailAPIView),
    path("tasks/<int:pk>/complete", views.taskCompletingAPIView),
    path("users", views.listUsersAPIView),
    path("users/profile", views.userProfileAPIView),
]
