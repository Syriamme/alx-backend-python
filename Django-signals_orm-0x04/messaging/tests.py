from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification, MessageHistory


class SignalTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='sender', password='testpass')
        self.user2 = User.objects.create_user(username='receiver', password='testpass')

    def test_notification_creation(self):
        """
        Create a notification
        """
        message = Message.objects.create(sender=self.user1, receiver=self.user2, content='Hello!')
        notification = Notification.objects.filter(user=self.user2, message=message).first()

        self.assertIsNotNone(notification)
        self.assertEqual(notification.user, self.user2)
        self.assertEqual(notification.message, message)
        self.assertFalse(notification.is_read)

class MessageEditTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password')
        self.user2 = User.objects.create_user(username='user2', password='password')

    def test_message_edit_tracks_user_and_time(self):
        """
        Create a message
        """
        message = Message.objects.create(sender=self.user1, receiver=self.user2, content="Hello")
        
        message.content = "Hello, edited!"
        message.edited = True
        message.edited_at = now()
        message.edited_by = self.user1
        message.save()

        self.assertTrue(message.edited)
        self.assertEqual(message.edited_by, self.user1)
        self.assertIsNotNone(message.edited_at)

class UserDeletionTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", password="password")
        self.user2 = User.objects.create_user(username="user2", password="password")

        # messages and notifications
        self.message = Message.objects.create(sender=self.user1, receiver=self.user2, content="Hello")
        self.notification = Notification.objects.create(user=self.user1, message="Notification")
        MessageHistory.objects.create(message=self.message, old_content="Original Content")

    def test_user_deletion_cleans_up_data(self):
        # Deleting the user
        self.user1.delete()

        # Checking related data is deleted
        self.assertFalse(Message.objects.filter(sender=self.user1).exists())
        self.assertFalse(Notification.objects.filter(user=self.user1).exists())
        self.assertFalse(MessageHistory.objects.filter(message__sender=self.user1).exists())