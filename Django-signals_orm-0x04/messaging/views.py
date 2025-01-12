from django.contrib.auth.models import User
from django.shortcuts import JsonResponse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from django.core.exceptions import ObjectDoesNotExist
from messaging.models import Message

@login_required
def delete_user(request):
    """
    Delete the currently logged-in user with error handling
    """
    if request.method == "POST":
        try:
            user = request.user
            if not user.is_authenticated:
                return JsonResponse({"error": "User is not authenticated"}, status=403)
            
            # Deleting the user and related data
            user.delete()
            return JsonResponse({"message": "User deleted successfully"})
        except ObjectDoesNotExist:
            return JsonResponse({"error": "User does not exist"}, status=404)
        except Exception as e:
            return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)
    return JsonResponse({"error": "Invalid request method"}, status=400)

@login_required
def unread_messages(request):
    """
    Display unread messages for
    the currently logged-in user.
    """
    user = request.user
    unread_msgs = Message.unread.unread_for_user(user).only('sender', 'content', 'timestamp')

    unread_msgs_list = [
        {
            'sender': msg.sender.username,
            'content': msg.content,
            'timestamp': msg.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        }
        for msg in unread_msgs
    ]
    
    return JsonResponse({'unread_messages': unread_msgs_list})

def fetch_threaded_conversation(request, message_id):
    """
    Fetch a message
    and its threaded replies recursively as JSON.
    """
    message = get_object_or_404(
        Message.objects.select_related('sender', 'receiver')
        .prefetch_related('replies'),
        id=message_id,
        sender=request.user
    )

    def get_replies(message):
        """
        Recursively fetch all replies to a message 
        and structure them as a dictionary.
        """
        replies = Message.objects.filter(parent_message=message).select_related('sender', 'receiver')
        return {
            "id": message.id,
            "sender": message.sender.username,
            "receiver": message.receiver.username,
            "content": message.content,
            "timestamp": message.timestamp.isoformat(),
            "replies": [get_replies(reply) for reply in replies]
        }

    conversation = get_replies(message)

    return JsonResponse({"conversation": conversation})

@login_required
@cache_page(60)
def conversation_view(request, conversation_id):
    """
    Display messages in a specific conversation
    and cache the view for 60 seconds.
    Returns the messages in JSON format.
    """
    user = request.user
    messages = Message.objects.filter(conversation_id=conversation_id).only('sender', 'content', 'timestamp')

    messages_data = [
        {
            'sender': message.sender.username,
            'content': message.content,
            'timestamp': message.timestamp.isoformat(),
        }
        for message in messages
    ]

    return JsonResponse({'messages': messages_data})