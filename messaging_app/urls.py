from django.urls import path, include

urlpatterns = [
    path("api/", include('chats.urls')),  # Add the chats app URLs under the /api/ prefix
]
