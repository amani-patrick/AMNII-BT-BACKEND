from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_analytics(request):
    """Fetch overall analytics for the user's trading activity."""
    # Replace this with real analytics logic
    data = {
        "total_trades": 100,
        "winning_trades": 70,
        "losing_trades": 30,
        "profit_loss": 1250.75,
        "average_trade_duration": "00:30:00",
    }
    return Response(data)
