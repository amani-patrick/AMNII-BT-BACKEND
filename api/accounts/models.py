from django.db import models
from django.contrib.auth.models import User

class TradingAccount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="trading_accounts")
    name = models.CharField(max_length=100)
    broker = models.CharField(max_length=100)
    account_number = models.CharField(max_length=50)
    broker_server = models.CharField(max_length=100)  # Added field for MT5 broker server
    balance = models.DecimalField(max_digits=15, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.broker} ({self.account_number})"
