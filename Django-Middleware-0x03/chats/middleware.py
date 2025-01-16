import datetime
import logging
from django.http import HttpResponseForbidden
from collections import defaultdict
from django.http import JsonResponse



class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
        #setting up the logger
        self.logger = logging.getLogger('django.request')
        handler = logging.FileHandler('user_requests.log')
        formatter = logging.Formatter('%(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    
    def __call__(self, request):
        """
        logging the request details
        """
        user =  request.user if request.user.is_authenticated else "Unknown"
        logging_message = f"{datetime.datetimenow()} - user: {user} - Path: {request.path}"
        self.logger.info(logging_message)

        response = self.get_response(request)
        return response

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response =  get_response

    def __call__(self, request):
        """
        Restrict access to message during this time
        """
        time_now = datetime.datetime.now.time()

        start_time_allowed  = datetime.time(18, 0)
        end_time_allowed = datetime.time(21, 0)

        if time_now < start_time_allowed or time_now > end_time_allowed:
            return HttpResponseForbidden("Restricted Chat access during this time")
        
        response = self.get_response(request)
        return response

class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

        # dictionary storing message count
        # and timestamp for each IP address

        self.request_logs = defaultdict(list)
        self.limit = 5
        self.time_set =  datetime.timedelta(minutes=1)

    def __call__(self, request):
        """
        Limit the POST requests (messages)
        """
        if request.method == "POST" and request.path.startswith("/chat"):
            ip_add = self.get_ip(request)

            current_time = datetime.datetime.now()

            self.request_logs[ip_add] = [
                timestamp
                for timestamp in self.request_logs[ip_add]
                if current_time - timestamp <= self.time_set
            ]

            if len(self.request_logs[ip_add]) >= self.limit:
                return JsonResponse(
                    {"error": "Rate limited for messaging exceeded"},
                    status=429
                )
            
            self.request_logs[ip_add].append(current_time)

        response = self.get_response(request)
        return response
    
    def get_ip(self, request):
        """
        Retrieving the client ip adddress
        based on their request
        """
        x_forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded:
            return x_forwarded.split(',')[0]
        return request.META.get('REMOTE_ADDR')

class  RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        """
        checks the user's role i.e admin,
        before allowing access to specific actions
        """

        restricted_paths = [
            "/chat/admin-action",
        ]
        if any(request.path.startswith(path) for path in restricted_paths)

        # checker whether user is authenticated
        user = request.user
        if not user.is_authenticated:
            return JsonResponse(
                {"error": "Authentication is required"},
                status=403
            )
        
        #modified based on where user's role is stored
        user_role = getattr(user, "role", None)

        if user_role not in ["admin", "moderator"]:
            return JsonResponse(
                {"error": "Not Authorized to access"},
                status=403
            )
        response = self.get_response(request)
        return response