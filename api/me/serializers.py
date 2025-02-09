from rest_framework import serializers
from django.contrib.auth.models import User
from api.orders import models
from rest_framework import serializers
from django.contrib.auth import get_user_model


class TradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Order 
        fields = ['id', 'symbol', 'status', 'created_at', 'entry_price', 'take_profit', 'stop_loss', 'quantity', 'pnl']


User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
