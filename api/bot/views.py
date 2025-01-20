from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def start_bot(request):
    """Start the trading bot."""
    # Add your bot-start logic here
    return Response({"message": "Bot started successfully!"})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def stop_bot(request):
    """Stop the trading bot."""
    # Add your bot-stop logic here
    return Response({"message": "Bot stopped successfully!"})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_bot_status(request):
    """Fetch the current status of the bot."""
    # Replace this with real status logic
    return Response({"status": "running"})
