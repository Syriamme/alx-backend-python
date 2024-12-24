from rest_framework import serializers
from .models import User, Conversation, Message

#UserSerializer for the user model
class UserSerializer(serializers.ModelSerializer):
    
    full_name = serializers.CharField(source='get_full_name', read_only=True)

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
    sender = serializers.SerializerMethodField()
    Conversation_id = serializers.PrimaryKeyRelatedField(
        queryset=Conversation.objects.all()
    )


    def the_sender(self, obj):
        """
        getting the full name of the sender
        and the email
        """
        return {
            'full_name': f"{obj.sender.first_name} {obj.sender.last_name}",
            'email': obj.sender.email,

        }
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
    participants = serializers.SerializerMethodField()
    messages = MessageSerializer(many=True, read_only=True)

    def the_participants(self, obj):
        """"
        returning a list o all the participant details
        """
        return UserSerializer(obj.participants.all(), many=True).data
    def validating(self, data):
        """"
        Validating to ensure that all conversations
        have atleast two participants
        """
        if'participants' in data  and len(data['participants']) < 2:
            raise serializers.ValidationError("atleast 2 participants in a conversation")
        return data

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
