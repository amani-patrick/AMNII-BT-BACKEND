import talib
import pandas as pd
from scipy.signal import argrelextrema

def calculate_pivot_points(data):
    """
    Calculate Pivot Points, Support, and Resistance levels.
    """
    high = data["high"]
    low = data["low"]
    close = data["close"]

    pivot_point = (high + low + close) / 3
    r1 = 2 * pivot_point - low
    s1 = 2 * pivot_point - high
    r2 = pivot_point + (high - low)
    s2 = pivot_point - (high - low)

    return pivot_point, r1, s1, r2, s2

def calculate_swing_levels(data, window=5):
    """
    Identify swing highs and lows as support and resistance levels.
    """
    highs = data["high"].values
    lows = data["low"].values

    # Find swing highs and lows using a rolling window
    swing_highs = argrelextrema(highs, comparator=lambda x, y: x > y, order=window)[0]
    swing_lows = argrelextrema(lows, comparator=lambda x, y: x < y, order=window)[0]

    return swing_highs, swing_lows

def calculate_atr_levels(data, atr_period=14):
    """
    Calculate ATR-based support and resistance buffer zones.
    """
    atr = talib.ATR(data["high"], data["low"], data["close"], timeperiod=atr_period)
    last_close = data["close"].iloc[-1]
    atr_value = atr.iloc[-1]

    # ATR levels
    support = last_close - atr_value
    resistance = last_close + atr_value

    return support, resistance

def calculate_trend(data, ema_period=50):
    """
    Calculate trend using EMA (Exponential Moving Average).
    """
    ema = talib.EMA(data["close"], timeperiod=ema_period)
    last_close = data["close"].iloc[-1]

    if last_close > ema.iloc[-1]:
        return "uptrend"
    elif last_close < ema.iloc[-1]:
        return "downtrend"
    else:
        return "range"

def identify_support_resistance(data):
    """
    Combine pivot points, swing levels, and ATR zones to define support and resistance.
    """
    pivot_point, r1, s1, r2, s2 = calculate_pivot_points(data)
    swing_highs, swing_lows = calculate_swing_levels(data, window=5)
    atr_support, atr_resistance = calculate_atr_levels(data)

    # Compile all levels
    levels = {
        "pivot_point": pivot_point.iloc[-1],
        "r1": r1.iloc[-1],
        "s1": s1.iloc[-1],
        "r2": r2.iloc[-1],
        "s2": s2.iloc[-1],
        "atr_support": atr_support,
        "atr_resistance": atr_resistance,
        "swing_highs": data["high"].iloc[swing_highs].values.tolist(),
        "swing_lows": data["low"].iloc[swing_lows].values.tolist(),
    }

    return levels

def strategy_with_trending_support_resistance(data):
    """
    Strategy that adapts support and resistance levels based on market trend.
    """
    # Detect trend
    trend = calculate_trend(data)
    levels = identify_support_resistance(data)

    last_close = data["close"].iloc[-1]
    action = None
    tp = None
    sl = None

    # Action based on trend
    if trend == "uptrend":
        # Buy near support (ATR support or swing lows), target resistance
        if last_close <= levels["atr_support"] or last_close <= min(levels["swing_lows"]):
            action = "Buy"
            tp = levels["r1"]  # Resistance level as TP
            sl = levels["atr_support"] - 0.0001  # SL below ATR support by 10 pips
        else:
            action = "Hold"
    elif trend == "downtrend":
        # Sell near resistance (ATR resistance or swing highs), target support
        if last_close >= levels["atr_resistance"] or last_close >= max(levels["swing_highs"]):
            action = "Sell"
            tp = levels["s1"]  # Support level as TP
            sl = levels["atr_resistance"] + 0.0001  # SL above ATR resistance by 10 pips
        else:
            action = "Hold"
    else:
        # In a range market, trade based on pivot points and swing highs/lows
        if last_close <= levels["s1"]:
            action = "Buy"
            tp = levels["r1"]  # Resistance as TP
            sl = levels["s2"]  # Support as SL
        elif last_close >= levels["r1"]:
            action = "Sell"
            tp = levels["s1"]  # Support as TP
            sl = levels["r2"]  # Resistance as SL
        else:
            action = "Hold"

    return {
        "action": action,
        "tp": tp,
        "sl": sl
    }
