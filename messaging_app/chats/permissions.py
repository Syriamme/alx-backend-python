from rest_framework.permissions import BasePermission

class IsParticipant(BasePermission):
    """
    Custom permission to allow access only
    if the user is part of the conversation.
    """

    def has_object_permission(self, request, view, obj):
        return obj.sender == request.user or obj.recipient == request.user
