import os
from django.core.wsgi import get_wsgi_application
from your_app_name.middleware import RequestLoggingMiddleware

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project_name.settings')

# Get the default WSGI application
django_wsgi_app = get_wsgi_application()

# Wrap it with your middleware
application = RequestLoggingMiddleware(django_wsgi_app)
