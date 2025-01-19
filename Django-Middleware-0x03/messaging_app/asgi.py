import os
from django.core.asgi import get_asgi_application
from your_app_name.middleware import RequestLoggingMiddleware

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project_name.settings')

# Get the default ASGI application
django_asgi_app = get_asgi_application()

# Wrap it with your middleware
application = RequestLoggingMiddleware(django_asgi_app)
