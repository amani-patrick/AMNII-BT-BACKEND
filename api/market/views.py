import MetaTrader5 as mt5
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# Initialize MetaTrader5 connection
if not mt5.initialize():
    print("Failed to initialize MetaTrader5")
    mt5.shutdown()

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_symbols(request):
    """Fetch available trading symbols."""
    symbols = ["GBPUSD", "EURUSD", "USDJPY", "USDCHF"]
    return Response(symbols)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_symbol_data(request, symbol):
    """Fetch live data for a specific symbol."""
    # Fetch live tick data using MetaTrader5
    tick = mt5.symbol_info_tick(symbol)

    if tick is None:
        return Response({"message": f"Failed to get live data for {symbol}"}, status=400)

    live_data = {
        "symbol": symbol,
        "bid": tick.bid,
        "ask": tick.ask,
        "last": tick.last,
        "time": tick.time
    }

    return Response(live_data)

mt5.shutdown()
