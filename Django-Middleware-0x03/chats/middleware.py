import logging
import time
from datetime import datetime
from django.http import HttpResponseForbidden
from collections import defaultdict

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        """
        Middleware initialization, receives the get_response callable.
        """
        self.get_response = get_response

    def __call__(self, request):
        """
        Logs the user's request with timestamp, user, and request path.
        """
        user = request.user.username if request.user.is_authenticated else 'Anonymous'
        path = request.path
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Log to file
        logger = logging.getLogger('request_logger')
        logger.info(f"{timestamp} - User: {user} - Path: {path}")
        
        # Call the next middleware or view
        response = self.get_response(request)
        return response
class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        """
        Initialize the middleware.
        """
        self.get_response = get_response

    def __call__(self, request):
        """
        Restrict access to the messaging app outside the hours of 9 AM to 6 PM.
        """
        current_time = datetime.now().hour  # Get the current hour (24-hour format)
        
        if current_time < 9 or current_time >= 18:
            # If it's before 9 AM or after 6 PM, deny access with a 403 Forbidden error
            return HttpResponseForbidden("Access to the messaging app is restricted outside of 9 AM to 6 PM.")
        
        # If it's within allowed hours, process the request normally
        response = self.get_response(request)
        return response
class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        """
        Initializes the middleware. Sets up an empty dictionary to track messages.
        """
        self.get_response = get_response
        # Dictionary to store IP addresses and their message timestamps
        self.ip_message_count = defaultdict(list)
        self.time_window = 60  # 60 seconds (1 minute) window
        self.message_limit = 5  # Maximum number of messages allowed per time window

    def __call__(self, request):
        """
        Middleware logic to track the number of POST requests (messages) per IP address.
        """
        # Only track POST requests (messages) to the chat
        if request.method == 'POST' and request.path.startswith('/chat/'):
            ip_address = request.META.get('REMOTE_ADDR')  # Get user's IP address
            current_time = time.time()  # Current time in seconds

            # Clean up timestamps outside of the time window
            self.ip_message_count[ip_address] = [
                timestamp for timestamp in self.ip_message_count[ip_address]
                if current_time - timestamp <= self.time_window
            ]

            # Check if the number of messages exceeds the limit
            if len(self.ip_message_count[ip_address]) >= self.message_limit:
                return HttpResponseForbidden("You have exceeded the message limit. Please try again later.")

            # Add the current timestamp to the user's message list
            self.ip_message_count[ip_address].append(current_time)

        # Process the request as usual
        response = self.get_response(request)
        return response

class RolePermissionMiddleware:
    def __init__(self, get_response):
        """
        Initializes the middleware. This stores the get_response callable.
        """
        self.get_response = get_response

    def __call__(self, request):
        """
        Middleware logic to check if the user has the appropriate role.
        Only users with 'admin' or 'moderator' roles are allowed to proceed.
        """
        # Check if the user is authenticated and has the required role
        if request.user.is_authenticated:
            user_roles = request.user.groups.values_list('name', flat=True)  # Retrieve user roles
            
            # If the user is neither an admin nor a moderator, deny access with 403
            if not any(role in user_roles for role in ['admin', 'moderator']):
                return HttpResponseForbidden("You do not have permission to perform this action.")
        else:
            # If the user is not authenticated, deny access
            return HttpResponseForbidden("You need to be logged in to perform this action.")

        # If the user has the correct role or is authenticated, process the request
        response = self.get_response(request)
        return response
