from django.contrib.auth.models import User
from django.shortcuts import JsonResponse, get_object_or_404
from django.contrib.auth.decorators import login_required
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
    Display unread messages for the
    currently logged-in user as a JSON response.
    """
    user = request.user
    unread_msgs = Message.unread.unread_for_user(user)

    messages_data = [
        {
            'sender': msg.sender.username,
            'content': msg.content,
            'timestamp': msg.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        }
        for msg in unread_msgs
    ]

    # Return the messages as a JSON response
    return JsonResponse({'unread_messages': messages_data})

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