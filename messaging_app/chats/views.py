from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework import status
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from .permissions import IsParticipantOfConversation

class ConversationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['participants__first_name', 'participants__last_name', 'participants__email']
    ordering_fields = ['created_at']


    def create(self, request, *args, **kwargs):
        """
        Creation of a new conversation
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        conversation = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['message_body', 'sender__first_name', 'sender__last_name']
    ordering_fields = ['created_at']
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]

    def list(self, request, *argz, **kwargz):
        """
        Listing the messages for each conversation
        """

        convesation_id = self.request.query_params.get('conversation_id')
        if not convesation_id:
            return Response(
                {"error": "conversation _id needed"},
                status = status.HTTP_400_BAD_REQUEST,
            )
        messg = Message.objects.filter(conversation_id=convesation_id)
        serialize= self.get_serializer(messg, many=True)
        return Response(serialize.data)

    def create(self, request, *args, **kwargs):
        """
        Sending message for a conversation.
        """
        convesation_id = request.data.get('conversation_id')
        conversation = get_object_or_404(Conversation, pk=convesation_id)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(conversation=conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
