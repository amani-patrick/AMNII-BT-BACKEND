import logging
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import AnalyticsSerializer
from api.orders.models import Order, MarketAnalytics
from django.db.models import Avg, Sum, F
from decimal import Decimal, InvalidOperation

# Set up logger
logger = logging.getLogger(__name__)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_analytics(request, symbol=None):
    """Fetch overall analytics for the user's trading activity, or specific symbol analytics."""
    user = request.user

    # If a symbol is provided, fetch symbol-based analytics
    if symbol:
        return get_symbol_analytics(request, symbol)
    
    # Otherwise, fetch overall analytics for the user
    trades = Order.objects.filter(user=user)

    total_trades = trades.count()

    # Winning and losing trades based on pnl (profit and loss)
    winning_trades = trades.filter(pnl__gt=0).count()  # Using pnl instead of profit
    losing_trades = trades.filter(pnl__lte=0).count()  # Using pnl instead of profit

    # Total profit or loss (net pnl)
    total_profit_loss = trades.aggregate(total_pnl=Sum('pnl'))['total_pnl']
    
    # Log the total_profit_loss value to debug
    logger.debug(f"Total Profit/Loss Value: {total_profit_loss}")
    
    # Safely check and convert total_profit_loss
    try:
        if total_profit_loss is None or isinstance(total_profit_loss, (str, bool)):
            total_profit_loss = Decimal(0)
        else:
            total_profit_loss = Decimal(total_profit_loss)
    except (InvalidOperation, TypeError) as e:
        logger.error(f"Error converting total_profit_loss to Decimal: {e}")
        total_profit_loss = Decimal(0)

    # Calculate average trade duration (ensure it is a valid number)
    trades_with_duration = trades.filter(completed_at__isnull=False)  # Ensure the order is completed
    average_trade_duration = trades_with_duration.aggregate(
        avg_duration=Avg(F('completed_at') - F('created_at'))
    )['avg_duration']
    
    # Log the average_trade_duration value to debug
    logger.debug(f"Average Trade Duration: {average_trade_duration}")
    
    # Check if the average duration is valid, and default to 0 if not
    if average_trade_duration is None:
        average_trade_duration = 0
    else:
        try:
            average_trade_duration = float(average_trade_duration)
        except (ValueError, TypeError) as e:
            logger.error(f"Error converting average_trade_duration to float: {e}")
            average_trade_duration = 0  # Default to 0 if invalid

    # Format duration (convert seconds to hours:minutes:seconds format)
    avg_duration_formatted = (
        f"{int(average_trade_duration // 3600):02}:{int((average_trade_duration % 3600) // 60):02}:{int(average_trade_duration % 60):02}"
        if average_trade_duration else "00:00:00"
    )

    # Prepare the response data
    data = {
        "total_trades": total_trades,
        "winning_trades": winning_trades,
        "losing_trades": losing_trades,
        "profit_loss": str(total_profit_loss),  # Convert Decimal to string
        "average_trade_duration": avg_duration_formatted,
    }

    # Serialize and return the response
    serializer = AnalyticsSerializer(data)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_symbol_analytics(request, symbol):
    """Fetch analytics for a specific symbol."""
    try:
        # Fetch the market analytics for the specific symbol
        market_analytics = get_object_or_404(MarketAnalytics, symbol=symbol)

        # Prepare the data response for the symbol
        data = {
            "name": market_analytics.symbol,
            "price": str(market_analytics.price),
            "profit": str(market_analytics.profit),
            "loss": str(market_analytics.loss),
            "neutral": str(market_analytics.neutral),
        }

        # Return the data as a JsonResponse (or Response for DRF)
        return Response(data)

    except MarketAnalytics.DoesNotExist:
        # If the symbol is not found in the MarketAnalytics model
        return JsonResponse({"error": "Symbol not found"}, status=404)
