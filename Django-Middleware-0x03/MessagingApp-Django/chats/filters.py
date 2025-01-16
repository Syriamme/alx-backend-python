from django_filters import rest_framework as filters
from .models import Message

class MessageFilter(filters.FilterSet):
    """
    A filter class to enable filtering messages
    based on the user or a time range
    """
    sender = filters.CharFilter(field_name='sender__username', lookup_expr='icontains')
    recipient = filters.CharFilter(field_name='conversation__participants__username', lookup_expr='icontains')
    date_after = filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    date_before = filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = Message
        fields = ['sender', 'recipient', 'date_after', 'date_before']
