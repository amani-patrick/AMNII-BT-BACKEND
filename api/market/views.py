from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_symbols(request):
    """Fetch available trading symbols."""
    # Replace with real market data logic
    symbols = ["EURUSD", "USDJPY", "GBPUSD", "BTCUSD"]
    return Response(symbols)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_symbol_data(request, symbol):
    """Fetch historical and live data for a specific symbol."""
    # Replace with real symbol data logic
    data = {
        "symbol": symbol,
        "price": 1.2345,
        "high": 1.2500,
        "low": 1.2200,
        "volume": 10000,
    }
    return Response(data)
