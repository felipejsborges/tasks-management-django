from django.urls import path

from . import views

urlpatterns = [path("sample/", views.hello_world, name="sample")]
