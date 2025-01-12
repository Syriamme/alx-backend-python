# messaging/managers.py

from django.db import models

class UnreadMessagesManager(models.Manager):
    """
    Custom manager to filter
    unread messages for a user.
    """
    def unread_for_user(self, user):
        return self.filter(receiver=user, read=False)
