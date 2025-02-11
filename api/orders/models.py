from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal


class Order(models.Model):
    ACTION_CHOICES = [('BUY', 'Buy'), ('SELL', 'Sell')]
    STATUS_CHOICES = [('PENDING', 'Pending'), ('COMPLETED', 'Completed'), ('CANCELED', 'Canceled')]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    symbol = models.CharField(max_length=10)
    entry_price = models.DecimalField(max_digits=10, decimal_places=5)
    take_profit = models.DecimalField(max_digits=10, decimal_places=5, null=True, blank=True)
    stop_loss = models.DecimalField(max_digits=10, decimal_places=5, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    action = models.CharField(max_length=4, choices=ACTION_CHOICES)
    pnl = models.DecimalField(max_digits=10, decimal_places=5, default=Decimal('0.00000'))
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.symbol} - {self.action}"

class MarketAnalytics(models.Model):
    symbol = models.CharField(max_length=20, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=4)
    profit = models.DecimalField(max_digits=5, decimal_places=2)
    loss = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.symbol