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
        return {
            "id": message.id,
            "sender": message.sender.username,
            "receiver": message.receiver.username,
            "content": message.content,
            "timestamp": message.timestamp.isoformat(),
            "replies": [get_replies(reply) for reply in message.replies.all()]
        }

    conversation = get_replies(message)

    return JsonResponse({"conversation": conversation})