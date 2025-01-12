def calculate_tp_sl(action, entry_price, pip_risk=10, pip_reward=30):
    pip_multiplier = 0.0001  
    if action == "BUY":
        sl = entry_price - (pip_risk * pip_multiplier)
        tp = entry_price + (pip_reward * pip_multiplier)
    elif action == "SELL":
        sl = entry_price + (pip_risk * pip_multiplier)
        tp = entry_price - (pip_reward * pip_multiplier)
    else:
        sl, tp = None, None
    return tp, sl
