from django.urls import path, include
from rest_framework import routers
from rest_framework_nested import routers
from .views import ConversationViewSet, MessageViewSet
from . import views

router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')

conversation_router = routers.NestedDefaultRouter(router, r'conversations', lookup='conversation')
conversation_router.register(r'messages', MessageViewSet, basename='conversation-messages')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/', include(conversation_router.urls)),
]
