from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.auth.hashers import make_password, check_password

class User(AbstractUser):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    phone_number = models.CharField(max_length=15, null=True, blank=True)
    role = models.CharField(
        max_length=10,
        choices=[('guest', 'Guest'), ('host', 'Host'), ('admin', 'Admin')],
        default='guest'
        )

    created_at = models.DateTimeField(auto_now_add=True)

    email = models.EmailField('email address', unique=True)

    password = models.CharField(max_length=255, null=False)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    groups = models.ManyToManyField(
        Group,
        related_name="customuser_groups",
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_permissions",
        blank=True
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"
    
    def get_full_name(self):
        """
        getting the user full names
        """
        return f"{self.first_name} {self.last_name}"

class Conversation(models.Model):
    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    participants = models.ManyToManyField(User, related_name='conversations')

    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        participants_names = ", ".join([user.email for user in self.participants.all()])
        return f"Conversation between: {participants_names}"
    
    def setting_password(self, raw_pass):
        """
        hashing the password
        """
        self.password = make_password(raw_pass)
    
    def checking_pass(self, raw_pass):
        """
        Validating the password
        """
        return check_password(raw_pass, self.password)

class Message(models.Model):
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')

    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')

    message_body = models.TextField()

    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.email} in Conversation {self.conversation.conversation_id}"
