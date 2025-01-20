from rest_framework import serializers

class AnalyticsSerializer(serializers.Serializer):
    total_trades = serializers.IntegerField()
    winning_trades = serializers.IntegerField()
    losing_trades = serializers.IntegerField()
    profit_loss = serializers.DecimalField(max_digits=15, decimal_places=2)
    average_trade_duration = serializers.DurationField()
