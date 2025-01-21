from alpha_vantage.foreignexchange import ForeignExchange
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import logging

logger = logging.getLogger(__name__)
API_KEY = 'RA9EAD30J57VC8IR'

# Supported forex pairs
SUPPORTED_PAIRS = ["GBPUSD", "EURUSD", "USDJPY", "USDCHF"]

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_forex_data(request, symbol):
    """Fetch live forex data for specific pairs from Alpha Vantage."""
    if symbol not in SUPPORTED_PAIRS:
        return Response({"message": "Invalid or unsupported currency pair."}, status=400)

    from_currency, to_currency = symbol[:3], symbol[3:]

    fx = ForeignExchange(key=API_KEY)
    try:
        data, _ = fx.get_currency_exchange_rate(from_currency=from_currency, to_currency=to_currency)
    except Exception as e:
        logger.error(f"Error fetching forex data: {e}")
        return Response({"message": f"Failed to fetch data for {symbol}"}, status=400)

    return Response(data)
