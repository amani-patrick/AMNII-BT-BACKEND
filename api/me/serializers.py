from rest_framework import serializers
from django.contrib.auth.models import User
from api.orders import models  # Ensure this import points to your correct Order model

class TradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Order  # Ensure this is the correct model
        fields = ['id', 'symbol', 'status', 'created_at', 'entry_price', 'take_profit', 'stop_loss', 'quantity', 'pnl']

class UserProfileSerializer(serializers.ModelSerializer):
    trades = TradeSerializer(many=True)  # Including related trades

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'profile_picture', 'trades']
