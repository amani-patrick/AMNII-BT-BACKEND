from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'user', 'title', 'message', 'created_at']  # Ensure 'user' is included

    def create(self, validated_data):
        # If user is required but not provided in the request, raise an error
        if 'user' not in validated_data:
            raise serializers.ValidationError({"user": "This field is required."})
        validated_data.setdefault('is_read', False)
        return super().create(validated_data)