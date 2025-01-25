from alpha_vantage.foreignexchange import ForeignExchange
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import CurrencyPair
import logging

# Set up logger
logger = logging.getLogger(__name__)

# API Key for Alpha Vantage
API_KEY = 'RA9EAD30J57VC8IR'

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_forex_data(request, symbol):
    """Fetch live forex data for specific pairs from Alpha Vantage."""
    
    try:
        currency_pair = CurrencyPair.objects.get(symbol=symbol)
        from_currency, to_currency = currency_pair.from_currency, currency_pair.to_currency

    except CurrencyPair.DoesNotExist:
        return Response({"message": "Invalid or unsupported currency pair."}, status=400)
    fx = ForeignExchange(key=API_KEY)

    try:
        data, _ = fx.get_currency_exchange_rate(from_currency=from_currency, to_currency=to_currency)
        exchange_rate = data.get('5. Exchange Rate', None)

        if exchange_rate is None:
            logger.error(f"No exchange rate found for {symbol}.")
            return Response({"message": f"Failed to fetch valid data for {symbol}."}, status=500)

    except Exception as e:
        logger.error(f"Error fetching forex data for {symbol}: {e}")
        return Response({"message": f"Failed to fetch data for {symbol}."}, status=500)

    return Response({"symbol": symbol, "exchange_rate": exchange_rate})
