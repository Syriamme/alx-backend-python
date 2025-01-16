from rest_framework.authentication import SessionAuthentication
from rest_framework.exceptions import AuthenticationFailed

class CustomSessionAuthentication(SessionAuthentication):

    def authenticate(self, request):
        """
        Custom SessionAuthentication class to add
        any custom authentication logic.
        """
        user_auth_tuple = super().authenticate(request)

        if user_auth_tuple is None:
            raise AuthenticationFailed('Authentication credentials were not provided.')

        return user_auth_tuple
