import MetaTrader5 as mt5
import logging
import time
from multiprocessing import Process
from utils import swing_highs_lows_res
from fetch_data import fetch_data as fetch
from .utils import calculate_tp_sl, check_dataframe, tick_info, progress_sleep, select_symbol
from strategy_1 import fvg_strategy  
from strategy_2 import sma_ema_strategy
from strategy_3 import strategy_with_trending_support_resistance
from strategy_4 import strategy_with_order_blocks

# Example symbol and setup
symbol = "EURUSD"
trade_count = 0
if not mt5.symbol_select(symbol, True):
    logging.error(f"Failed to select symbol {symbol}")
    progress_sleep(0)

select_symbol(symbol)

def execute_trade(action, tp, sl):
    """
    Function to execute the trade based on action, TP, and SL.
    """
    global trade_count

    if action == "Buy" and trade_count < 5:
        price = tick_info.ask
        trade_request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": 0.01,
            "type": mt5.ORDER_TYPE_BUY,
            "price": price,
            "tp": float(tp),
            "sl": float(sl),
            "comment": "AutoTrade",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        result = mt5.order_send(trade_request)
        if result is None or result.retcode != mt5.TRADE_RETCODE_DONE:
            logging.error("Order send failed, no result returned by MetaTrader5.")
        else:
            logging.info(f"TRADE SUCCESSFUL: Buy on {symbol} at {price} with TP: {tp} and SL: {sl}")
            trade_count += 1

    elif action == "Sell" and trade_count < 5:
        price = tick_info.bid
        trade_request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": 0.01,
            "type": mt5.ORDER_TYPE_SELL,
            "price": float(price),
            "tp": float(tp),
            "sl": float(sl),
            "comment": "AutoTrade",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        result = mt5.order_send(trade_request)
        if result is None or result.retcode != mt5.TRADE_RETCODE_DONE:
            logging.error("Order send failed, no result returned by MetaTrader5.")
        else:
            logging.info(f"TRADE SUCCESSFUL: Sell on {symbol} at {price} with TP: {tp} and SL: {sl}")
            trade_count += 1
    else:
        logging.info("Trade count exceeded or action is Hold.")

def run_strategy(strategy_function):
    """
    Run a given strategy function and execute trades accordingly.
    """
    data = fetch(symbol)
    swing_highs_lows = swing_highs_lows_res(data) 
    result = strategy_function(data, swing_highs_lows)
    action = result.get("action")
    tp = result.get("tp")
    sl = result.get("sl")

    if action != "Hold" and tp is not None and sl is not None:
        execute_trade(action, tp, sl)  

if __name__ == '__main__':
    strategies = [
        fvg_strategy,
        sma_ema_strategy,
        strategy_with_trending_support_resistance,
        strategy_with_order_blocks
    ]

    processes = []
    for strategy in strategies:
        p = Process(target=run_strategy, args=(strategy,))
        p.start()
        processes.append(p)

    try:
        while any(p.is_alive() for p in processes):
            time.sleep(60) 
    except KeyboardInterrupt:
        logging.info("Shutting down processes...")
        for p in processes:
            p.terminate()
