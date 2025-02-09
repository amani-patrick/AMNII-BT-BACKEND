from rest_framework import serializers
from .models import TradingAccount

class TradingAccountSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    password = serializers.CharField(write_only=True)  # To securely handle the password

    class Meta:
        model = TradingAccount
        fields = ['id', 'user', 'name', 'broker', 'account_number', 'broker_server', 'balance', 'created_at', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        account = super().create(validated_data)

        # Set the password if provided and hash it
        if password:
            account.set_password(password)
            account.save()

        return account

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)

        # Update fields as usual
        instance = super().update(instance, validated_data)

        # If a new password is provided, hash and update it
        if password:
            instance.set_password(password)
            instance.save()

        return instance
