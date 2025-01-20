from alpha_vantage.foreignexchange import ForeignExchange
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.crypto import CryptoCurrencies
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import logging

# Configure logging
logger = logging.getLogger(__name__)

# Alpha Vantage API key (replace with your own)
API_KEY = 'YOUR_ALPHA_VANTAGE_API_KEY'

# Fetch real-time forex data
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_forex_data(request, symbol):
    """Fetch live forex data from Alpha Vantage."""
    # Determine the base and quote currency from the symbol
    from_currency, to_currency = symbol[:3], symbol[3:]

    # Initialize ForeignExchange API
    fx = ForeignExchange(key=API_KEY)
    try:
        data, _ = fx.get_currency_exchange_rate(from_currency=from_currency, to_currency=to_currency)
    except Exception as e:
        logger.error(f"Error fetching forex data: {e}")
        return Response({"message": f"Failed to fetch data for {symbol}"}, status=400)

    return Response(data)

# Fetch real-time stock data
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_stock_data(request, symbol):
    """Fetch real-time stock data from Alpha Vantage."""
    # Initialize TimeSeries API
    ts = TimeSeries(key=API_KEY, output_format='json')
    try:
        data, _ = ts.get_quote_endpoint(symbol=symbol)
    except Exception as e:
        logger.error(f"Error fetching stock data: {e}")
        return Response({"message": f"Failed to fetch data for {symbol}"}, status=400)

    return Response(data)

# Fetch real-time cryptocurrency data
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_crypto_data(request, symbol):
    """Fetch real-time cryptocurrency data from Alpha Vantage."""
    # Example: BTCUSD, ETHUSD
    crypto_symbol, market_symbol = symbol[:3], symbol[3:]

    # Initialize CryptoCurrencies API
    crypto = CryptoCurrencies(key=API_KEY)
    try:
        data, _ = crypto.get_digital_currency_rate(
            market_symbol=market_symbol, 
            digital_currency_symbol=crypto_symbol, 
            market='USD'
        )
    except Exception as e:
        logger.error(f"Error fetching crypto data: {e}")
        return Response({"message": f"Failed to fetch data for {symbol}"}, status=400)

    return Response(data)
