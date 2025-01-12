import MetaTrader5 as mt5
import pandas as pd
import trade_logic.fetch_data as fetch
import talib
import trade_logic.utils
from trade_logic.utils import calculate_tp_sl
from trade_logic.strategy_1 import symbol

data=fetch(symbol)

def sma_ema_strategy(data, sma_period=20, ema_period=50, variable="close", adx_period=14):
    data["SMA"] = talib.SMA(data[variable], timeperiod=sma_period)
    data["EMA"] = talib.EMA(data[variable], timeperiod=ema_period)
    data["ADX"] = talib.ADX(data["high"], data["low"], data["close"], timeperiod=adx_period)
    last_3 = data.iloc[-3:]  # Get the last 3 rows
    crossover_buy = (
        (last_3["SMA"].iloc[-2] <= last_3["EMA"].iloc[-2]) & 
        (last_3["SMA"].iloc[-1] > last_3["EMA"].iloc[-1]) &   
        (last_3["ADX"].iloc[-1] > 25)                       
    )
    crossover_sell = (
        (last_3["SMA"].iloc[-2] >= last_3["EMA"].iloc[-2]) &  
        (last_3["SMA"].iloc[-1] < last_3["EMA"].iloc[-1]) &  
        (last_3["ADX"].iloc[-1] > 25)                        
    )
    if crossover_buy:
        action = "BUY"
    elif crossover_sell:
        action = "SELL"
    else:
        action = "No Action"

    return action, data.iloc[-1]["close"]
def determine_trade_action():

    action, entry_price = sma_ema_strategy(data)

    if action in ["Buy", "Sell"]:
        take_profit, stop_loss = calculate_tp_sl(action, entry_price)
    else:
        take_profit, stop_loss = None, None

    return {
        "action": action,
        "tp": take_profit,
        "sl": stop_loss
    }