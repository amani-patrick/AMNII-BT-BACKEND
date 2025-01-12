import MetaTrader5 as mt5
import pandas as pd
import numpy as np
import os
from dotenv import load_dotenv

load_dotenv()

login = int(os.getenv('LOGIN'))
server = os.getenv('SERVER')
password = os.getenv('PASSWORD')

if not login or not server or not password:
    raise ValueError("Missing required MetaTrader5 credentials.")

if not mt5.initialize(login, password, server):
    raise RuntimeError(f"Initialize() failed, error code = {mt5.last_error()}")

def fetch_data(self,symbol):
    rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M15, 0, 48)
    data = pd.DataFrame(rates)
    data['time'] = pd.to_datetime(data['time'], unit='s')
    data['volume'] = data['tick_volume']
    del data['real_volume']
    del data['spread']
    del data['tick_volume']
    data.set_index(data['time'], inplace=True)
    data1 = data[['open', 'high', 'low', 'close', 'volume']]
    return data1


