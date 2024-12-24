from rest_framework import serializers
from .models import User, Conversation, Message

#UserSerializer for the user model
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'user_id',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'role',
            'created_at'
        ]
        read_only_fields = [
            'user_id',
            'created_at'
        ]

#Message serializer for the message model
class MessageSerializer(serializers.ModelSerializers):
    sender = UserSerializer(read_only=True)
    Conversation_id = serializers.PrimarykeyRelatedField(queryset=Conversation.objects.all())

    class Meta:
        model=Message
        fields = [
            'message_id',
            'sender',
            'message_body',
            'sent_at',
            'conversation_id'
        ]

class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model=Conversation
        fields = [
            'convsersation_id',
            'participants',
            'messages',
            'created_at'
        ]

        read_only_fields= [
            'conversation_id',
            'created_at'
        ]
