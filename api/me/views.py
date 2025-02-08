from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import UserProfileSerializer, TradeSerializer
from api.orders.models import Order  # 

@api_view(['GET'])
def me_view(request):
    if not request.user.is_authenticated:
        return Response({"detail": "Authentication credentials were not provided."}, status=401)
    user = request.user
    trades = Order.objects.filter(user=user)
    balance = user.profile.balance if hasattr(user, 'profile') else 0
    user_data = UserProfileSerializer(user, context={'request': request}).data
    user_data['trades'] = TradeSerializer(trades, many=True).data
    user_data['balance'] = balance
    
    return Response(user_data)
