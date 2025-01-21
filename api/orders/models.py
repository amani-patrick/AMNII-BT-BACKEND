from django.db import models
from django.utils import timezone

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    order_id = models.CharField(max_length=50, unique=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='orders')
    symbol = models.CharField(max_length=20)
    order_type = models.CharField(max_length=10)  # 'buy' or 'sell'
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # New fields
    profit = models.DecimalField(max_digits=15, decimal_places=2, default=0)  # Assumed profit field
    start_time = models.DateTimeField()  # When the trade started
    end_time = models.DateTimeField(null=True, blank=True)  # When the trade ended (can be null if still open)

    def __str__(self):
        return f"{self.symbol} - {self.order_id}"
    
    @property
    def duration(self):
        if self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return (timezone.now() - self.start_time).total_seconds()  # If trade is still open, use current time
