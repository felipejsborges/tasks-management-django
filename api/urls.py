from django.urls import path

from . import views

urlpatterns = [
    path("tasks", views.taskListAPIView),
    path("tasks/<int:pk>", views.taskDetailAPIView),
    path("users", views.userCreateAPIView),
    path("users/profile", views.userProfileAPIView),
]
