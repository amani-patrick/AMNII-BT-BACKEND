import smartmoneyconcepts as smc
import MetaTrader5 as mt5
from .strategy_1 import fvg_res
import fetch_data as fetch
from execute import data
import datetime,time
import tqdm
from ..models import Trade,Market_data,Portfolio





symbol = "EURUSD"

swing_highs_lows_res = smc.swing_highs_lows(data[['open', 'high', 'low', 'close', 'volume']], swing_length=20)


def progress_sleep(seconds):
    """
    Displays a single progress bar for the specified time duration.
    :param seconds: Total time to wait, in seconds.
    """
    with tqdm.tqdm(total=seconds, desc="Waiting for next order", unit="s", leave=True) as pbar:
        for _ in range(seconds):
            time.sleep(1)
            pbar.update(1)
def select_symbol(symbol):
    if not mt5.symbol_select(symbol, True):
        raise RuntimeError(f"Failed to select symbol {symbol}")
def tick_info(symbol):
    tick_info=mt5.symbol_info_tick(symbol)
    return tick_info
def check_dataframe(current_price_data):
    required_columns = ['FVG', 'Top', 'Bottom', 'MitigatedIndex']
    for col in required_columns:
        if col not in fvg_res.columns:
            raise ValueError(f"Missing required column: {col}")
    if 'low' not in current_price_data:
            raise ValueError("Current price data must contain a 'low' key.")
        
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

# my_app/utils.py



def initialize_portfolio(user):
    if not hasattr(user, 'portfolio'):
        Portfolio.objects.create(user=user, balance=1000.0)

def log_trade(user, symbol, price, volume, trade_type, tp_price, sl_price, strategy, pips_atrisk):
    portfolio = user.portfolio
    trade = Trade.objects.create(
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

def update_market_data(symbol, data):
    Market_data.objects.create(symbol=symbol, data=data)
