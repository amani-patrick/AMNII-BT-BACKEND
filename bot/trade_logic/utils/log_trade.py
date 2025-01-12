from bot import models

def log_trade(user, symbol, price, volume, trade_type, tp_price, sl_price, strategy, pips_atrisk):
    portfolio = user.portfolio
    trade = models.Trade.objects.create(
        portfolio=portfolio,
        symbol=symbol,
        price=price,
        volume=volume,
        trade_type=trade_type,
        tp_price=tp_price,
        sl_price=sl_price,
        strategy=strategy,
        pips_atrisk=pips_atrisk
    )
    return trade