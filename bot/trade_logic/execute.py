import MetaTrader5 as mt5
import logging
import time,os
from multiprocessing import Process
from bot.trade_logic import fetch_data as fetch
from bot.trade_logic.utils import calculate_tp_sl,check_dataframe,log_trade,portfolio,progress_sleep,select_symbol,symbol,tick_info
from bot.trade_logic import fetch_data
from bot.trade_logic.utils import smc_indicators_res
from bot.trade_logic import strategy_1,strategy_2,strategy_3,strategy_4
from dotenv import load_dotenv

load_dotenv()

login = int(os.getenv('LOGIN'))
server = os.getenv('SERVER')
password = os.getenv('PASSWORD')
if not mt5.initialize():
    logging.error("MetaTrader 5 initialization failed.")
    exit(1)
swing_highs_lows_res,fvg_res,ob_res,prev_high_low_res = smc_indicators_res(fetch_data(symbol))

# Example symbol and setup
symbol = "EURUSD"
trade_count = 0
select_symbol(symbol)

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
        strategy_1,
        strategy_2,
        strategy_3,
        strategy_4,
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
