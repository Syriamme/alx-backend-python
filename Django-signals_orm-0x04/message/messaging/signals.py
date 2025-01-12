from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message, Notification

@receiver(post_save, sender=Message)
def created_notification(sender, instance, created, **kwargs):
    """
    notification whenever message is created
    """
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )