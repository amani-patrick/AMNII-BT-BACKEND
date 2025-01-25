from django.db import models
from django.utils import timezone
from decimal import Decimal

class Order(models.Model):
    PENDING = 'pending'
    COMPLETED = 'completed'
    CANCELED = 'canceled'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (COMPLETED, 'Completed'),
        (CANCELED, 'Canceled'),
    ]

    id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    canceled_at = models.DateTimeField(null=True, blank=True)
    entry_price = models.DecimalField(max_digits=10, decimal_places=2)
    take_profit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stop_loss = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    quantity = models.PositiveIntegerField()
    pnl = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Optional, only if you want to store it

    def __str__(self):
        return f"Order {self.id} - {self.status} at {self.entry_price}"

