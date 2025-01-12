from django.db import models
from django.contrib.auth.models import User

class Portfolio(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=12,decimal_places=5,default=0.0)

class Trade(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE,related_name='trades')
    symbol=models.CharField(max_length=10)
    price=models.FloatField(max_length=10,decimal_places=5)
    volume= models.DecimalField(max_length=3,decimal_places=3)
    trade_type=models.CharField(max_length=10,choices=[('Buy', 'BUY'),('Sell', 'SELL')])
    tp_price=models.FloatField(max_length=10,decimal_places=5)
    sl_price=models.FloatField(max_length=10,decimal_places=5)
    pips_atrisk=models.DecimalField(max_length=2,decimal_places=0)
    profit_loss=models.DecimalField(max_length=12,decimal_places=5,default=0.0)
    strategy = models.CharField(max_length=20, choices=[
        ('strategy_1', 'Strategy 1'),
        ('strategy_2', 'Strategy 2'),
        ('strategy_3', 'Strategy 3'),
        ('strategy_4', 'Strategy 4'),
    ])
    class Meta:
        ordering = ['-timestamp']   

    def __str__(self):
        return self.symbol

    def save(self, *args, **kwargs):
        if self.trade_type == 'BUY':
            self.portfolio.balance -= self.volume * self.price
            self.portfolio.save()
        elif self.trade_type == 'SELL':
            self.portfolio.balance += self.volume * self.price
            self.portfolio.save()
        super().save(*args, **kwargs)

class Market_data(models.Model):
    symbol=models.CharField(max_length=10)
    data=models.JSONField(default=dict)
    timestamp=models.Datetimefield(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return self.symbol

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        Market_data.objects.all().order_by('-timestamp').exclude(id=self.id).delete()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        Market_data.objects.all().order_by('-timestamp').exclude(id=self.id).delete()

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
        Market_data.objects.all().order_by('-timestamp').exclude(id=self.id).delete()

    def create(self, *args, **kwargs):
        super().create(*args, **kwargs)
