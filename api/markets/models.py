from django.db import models

class CurrencyPair(models.Model):
    """Model to store supported currency pairs."""
    from_currency = models.CharField(max_length=3)
    to_currency = models.CharField(max_length=3)   
    symbol = models.CharField(max_length=7, unique=True)  
    def __str__(self):
        return f"{self.from_currency}{self.to_currency}"

    class Meta:
        verbose_name = "Currency Pair"
        verbose_name_plural = "Currency Pairs"
