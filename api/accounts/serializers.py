from rest_framework import serializers
from .models import TradingAccount

class TradingAccountSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    password = serializers.CharField(write_only=True)  # To securely handle the password

    class Meta:
        model = TradingAccount
        fields = ['id', 'user', 'name', 'broker', 'account_number', 'broker_server', 'balance', 'created_at']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        account = super().create(validated_data)
        
        if password:
            account.set_password(password) 
            account.save()

        return account
