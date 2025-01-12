from django.contrib.auth.models import User
from django.shortcuts import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

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
