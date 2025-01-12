from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification

class SignalTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='sender', password='testpass')
        self.user2 = User.objects.create_user(username='receiver', password='testpass')

    def test_notification_creation(self):
        message = Message.objects.create(sender=self.user1, receiver=self.user2, content='Hello!')
        notification = Notification.objects.filter(user=self.user2, message=message).first()

        self.assertIsNotNone(notification)
        self.assertEqual(notification.user, self.user2)
        self.assertEqual(notification.message, message)
        self.assertFalse(notification.is_read)
