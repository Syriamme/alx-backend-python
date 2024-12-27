
from rest_framework.permissions import BasePermission, IsAuthenticated

class IsParticipantOfConversation(BasePermission):

    def has_permission(self, request, view):
        """
        Custom permission to allow
        users to access their own messages only.
        """
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return request.user in obj.conversation.participants.all()
