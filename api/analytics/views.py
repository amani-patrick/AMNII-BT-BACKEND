from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from orders.models import Order  # Import your Order model
from django.db.models import Avg, Count, Sum

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_analytics(request):
    """Fetch overall analytics for the user's trading activity."""
    user = request.user  

    trades = Order.objects.filter(user=user)  # Assuming Order has a user ForeignKey
    total_trades = trades.count()
    winning_trades = trades.filter(profit__gt=0).count()
    losing_trades = trades.filter(profit__lte=0).count()
    profit_loss = trades.aggregate(total_profit=Sum('profit'))['total_profit'] or 0
    average_trade_duration = trades.aggregate(avg_duration=Avg('duration'))['avg_duration'] or 0

    # Format duration (assuming `duration` is stored as seconds in the model)
    avg_duration_formatted = str(average_trade_duration // 3600).zfill(2) + ":" + \
                             str((average_trade_duration % 3600) // 60).zfill(2) + ":" + \
                             str(average_trade_duration % 60).zfill(2)

    data = {
        "total_trades": total_trades,
        "winning_trades": winning_trades,
        "losing_trades": losing_trades,
        "profit_loss": profit_loss,
        "average_trade_duration": avg_duration_formatted,
    }

    return Response(data)
