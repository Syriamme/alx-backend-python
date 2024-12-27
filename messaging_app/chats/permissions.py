from rest_framework.permissions import BasePermission

class IsOwnerOrReadOnly(BasePermission):
    """
    Custom permission to allow
    users to access their own messages only.
    """

    def has_object_permission(self, request, view, obj):
        return obj.sender == request.user or obj.recipient == request.user
