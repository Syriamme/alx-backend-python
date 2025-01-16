# chats/middleware.py

import logging
from datetime import datetime

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
