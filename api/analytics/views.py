from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import AnalyticsSerializer
from api.orders.models import Order  

from django.db.models import Avg, Sum

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_analytics(request):
    """Fetch overall analytics for the user's trading activity."""
    user = request.user

    trades = Order.objects.filter(user=user)  
    total_trades = trades.count()
    winning_trades = trades.filter(profit__gt=0).count()  # Assuming `profit` exists as a field in the model
    losing_trades = trades.filter(profit__lte=0).count()  # Assuming `profit` exists as a field in the model
    profit_loss = trades.aggregate(total_profit=Sum('profit'))['total_profit'] or 0  # Handles `None` gracefully
    average_trade_duration = trades.aggregate(avg_duration=Avg('duration'))['avg_duration'] or 0  # Handles `None` gracefully

    # Format duration (assuming `duration` is stored as seconds in the model)
    avg_duration_formatted = (
        f"{int(average_trade_duration // 3600):02}:{int((average_trade_duration % 3600) // 60):02}:{int(average_trade_duration % 60):02}"
    )

    # Prepare the response data
    data = {
        "total_trades": total_trades,
        "winning_trades": winning_trades,
        "losing_trades": losing_trades,
        "profit_loss": profit_loss,
        "average_trade_duration": avg_duration_formatted,
    }
    serializer = AnalyticsSerializer(data)

    return Response(serializer.data)
