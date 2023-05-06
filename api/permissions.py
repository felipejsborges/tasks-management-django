from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow owners (or admin) of an object to edit it.
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in ("HEAD", "OPTIONS"):
            return True
        if request.user.is_superuser:
            return True
        if obj.owner == request.user:
            return True
        return False
