import MetaTrader5 as mt5
def tick_info(symbol):
    tick_info=mt5.symbol_info_tick(symbol)
    return tick_info