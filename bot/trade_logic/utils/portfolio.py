from bot import models

def initialize_portfolio(user):
    if not hasattr(user, 'portfolio'):
        models.Portfolio.objects.create(user=user, balance=100.0)