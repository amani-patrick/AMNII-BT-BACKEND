from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Notification

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_notifications(request):
    """Fetch notifications for the authenticated user."""
    notifications = Notification.objects.filter(user=request.user).values('id', 'message', 'created_at')
    return Response(list(notifications))


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_notification(request):
    """Create a new notification (admin use only)."""
    message = request.data.get('message')
    if not message:
        return Response({"detail": "Message is required"}, status=400)
    Notification.objects.create(user=request.user, message=message)
    return Response({"message": "Notification created successfully!"})
