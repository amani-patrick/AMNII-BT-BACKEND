import MetaTrader5 as mt5
import logging
from bot.trade_logic.utils import progress_sleep
def select_symbol(symbol):
    if not mt5.symbol_select(symbol, True):
        logging.error(f"Failed to select symbol {symbol}")
        progress_sleep(0)