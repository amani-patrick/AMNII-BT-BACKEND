from django.db import models
from django.contrib.auth.models import User


class Order(models.Model):
    # Order-related fields
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    order_id = models.CharField(max_length=100, unique=True)  # Unique order identifier
    symbol = models.CharField(max_length=10)  # Trading pair or product symbol, e.g., "GBPUSD"
    order_type = models.CharField(
        max_length=10,
        choices=[("BUY", "Buy"), ("SELL", "Sell")],
        default="BUY"
    )
    quantity = models.DecimalField(max_digits=10, decimal_places=2)  # Quantity of asset
    price = models.DecimalField(max_digits=20, decimal_places=6)  # Price per unit
    status = models.CharField(
        max_length=15,
        choices=[
            ("PENDING", "Pending"),
            ("COMPLETED", "Completed"),
            ("CANCELED", "Canceled"),
        ],
        default="PENDING",
    )
    timestamp = models.DateTimeField(auto_now_add=True)  # Order creation time
    updated_at = models.DateTimeField(auto_now=True)  # Last updated time

    # Optional fields
    stop_loss = models.DecimalField(
        max_digits=20, decimal_places=6, null=True, blank=True
    )  # Stop loss price
    take_profit = models.DecimalField(
        max_digits=20, decimal_places=6, null=True, blank=True
    )  # Take profit price

    class Meta:
        ordering = ["-timestamp"]
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def __str__(self):
        return f"Order {self.order_id} ({self.user.username}) - {self.symbol} ({self.order_type})"
