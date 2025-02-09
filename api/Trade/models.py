from django.db import models
from django.utils import timezone
from decimal import Decimal
from django.contrib.auth.models import User

class Order(models.Model):
    PENDING = 'pending'
    COMPLETED = 'completed'
    CANCELED = 'canceled'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (COMPLETED, 'Completed'),
        (CANCELED, 'Canceled'),
    ]

    BUY = 'buy'
    SELL = 'sell'

    ACTION_CHOICES = [
        (BUY, 'Buy'),
        (SELL, 'Sell'),
    ]

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")  # Added user field
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    canceled_at = models.DateTimeField(null=True, blank=True)
    entry_price = models.DecimalField(max_digits=10, decimal_places=2)
    take_profit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stop_loss = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    quantity = models.PositiveIntegerField()
    pnl = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    symbol = models.CharField(max_length=20)
    action = models.CharField(max_length=4, choices=ACTION_CHOICES, default=BUY)   

    def __str__(self):
        return f"Order {self.id} - {self.symbol} - {self.action} - {self.status} at {self.entry_price}" 

    def save(self, *args, **kwargs):
        self.action = self.action.lower() 
        super().save(*args, **kwargs)
