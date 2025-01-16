import MetaTrader5 as mt5
import pandas as pd
import numpy as np
import os
from dotenv import load_dotenv
import time
import logging

load_dotenv()

class Trade:
    def __init__(self):
        """
        Initializes the Trade class.
        """
        self.account = None
        self.symbols = ['GBPUSD','EURUSD','USDJPY','USDCHF','AUDUSD','USDCAD']
        self.log_file = "Trade_log.txt"
        self.login=os.getenv('LOGIN')
        self.password=os.getenv('PASSWORD')
        self.server=os.getenv('SERVER')
        self.balance= None

    def login_mt5(self, login, password, server):
        """
        Logs into the MT5 account.
        """
        if not mt5.initialize():
            raise Exception("Failed to initialize MT5")
        if not mt5.login(login, password=password, server=server):
            raise Exception(f"Login failed. Error: {mt5.last_error()}")
        authorize=mt5.login(login,password)
        if authorize:
            self.account = mt5.account_info()
            if self.account is not None:
                account_info=self.account._asdict()
                self.balance = account_info('balance', 'N/A')
                currency = account_info('currency', 'N/A')
            else:
                logging.info(mt5.last_error())

    def fetch_data(self, symbol, timeframe, start_time, end_time):
        """
        Fetches historical data for a given symbol and timeframe.
        """
        rates =  mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M15, 0, 72)
        if rates is None:
            logging.info("Failed to retrieve data from online")
            raise Exception(f"Failed to fetch data. Error: {mt5.last_error()}")
        data = pd.DataFrame(rates)
        data['time'] = pd.to_datetime(data['time'], unit='s')
        data['volume'] = data['tick_volume']
        del data['real_volume']
        del data['spread']
        del data['tick_volume']
        data.set_index(data['time'], inplace=True)
        data1 = data[['open', 'high', 'low', 'close', 'volume']]
        return data1

    def calculate_tp_sl(self, entry_price, symbol, risk_percent=1):
        """
        Calculates take-profit and stop-loss levels based on entry price and symbol.
        Parameters:
        - entry_price: The price at which the trade is opened.
        - symbol: The currency pair (e.g., 'EURUSD', 'GBPUSD').
        - risk_percent: The percentage of the account balance to risk per trade (default is 1%).
        
        Returns:
        - tp: The take-profit price level.
        - sl: The stop-loss price level.
        """

        # Define pip values for each currency pair
        pip_values = {
            'GBPUSD': 0.10,  # 0.01 lot size, 1 pip = $0.10
            'EURUSD': 0.10,
            'USDJPY': 0.10,
            'USDCHF': 0.10,
            'AUDUSD': 0.10,
            'USDCAD': 0.10
        }

        # Ensure the symbol is valid
        if symbol not in pip_values:
            raise ValueError(f"Invalid symbol: {symbol}. Supported symbols are: {', '.join(pip_values.keys())}")

        # Get pip value for the given symbol
        pip_value = pip_values[symbol]

        # Account risk calculation (based on a $20 account)
        account_balance = 20  # Account balance in dollars
        risk_amount = account_balance * (risk_percent / 100)  # Risk in dollars

        # Calculate the number of pips to risk (based on pip value and risk amount)
        stop_loss_pips = risk_amount / pip_value

        # Define take profit range (based on a 1:2 or 1:3 risk-to-reward ratio)
        take_profit_pips = stop_loss_pips * 2  # Risk-to-reward ratio of 1:2

        # Adjust entry price based on stop-loss and take-profit
        sl = entry_price - stop_loss_pips * 0.0001
        tp = entry_price + take_profit_pips * 0.0001

        return tp, sl


    def log_trade(self, message):
        """
        Logs trade-related information.
        """
        with open(self.log_file, "a") as f:
            f.write(f"{time.ctime()} - {message}\n")

    def portfolio(self):
        """
        Returns portfolio information.
        """
        return mt5.account_info()

    def progress_sleep(self, seconds):
        """
        Sleeps for a given duration, showing progress.
        """
        for _ in range(seconds):
            print(".", end="", flush=True)
            time.sleep(1)
        print()

    def select_symbol(self, symbol):
        """
        Selects and checks a symbol for trading.
        """
        if not mt5.symbol_select(symbol, True):
            raise Exception(f"Failed to select symbol: {symbol}")
        self.symbols.append(symbol)

    def fetch_tick_info(self, symbol):
        """
        Fetches tick information for the given symbol.
        """
        tick = mt5.symbol_info_tick(symbol)
        if tick is None:
            raise Exception(f"Failed to fetch tick info for {symbol}. Error: {mt5.last_error()}")
        return tick

    def fetch_account_details(self):
        """
        Fetches account details.
        """
        account_info = mt5.account_info()
        if account_info is None:
            raise Exception(f"Failed to fetch account details. Error: {mt5.last_error()}")
        return account_info

    def fvg_strategy(self, symbol):
        """
        Implements a Fair Value Gap (FVG) trading strategy.
        """
        pass

    def sma_ema_strategy(self, symbol, sma_period, ema_period):
        """
        Implements a Simple Moving Average (SMA) and Exponential Moving Average (EMA) strategy.
        """
        pass

    def support_resistance_strategy(self, symbol):
        """
        Implements a support and resistance trading strategy.
        """
        pass

    def order_block_strategy(self, symbol):
        """
        Implements an order block trading strategy.
        """
        pass

    def main(self):
        """
        Main entry point for the program.
        """
        try:
            print("Logging into MT5...")
            self.login_mt5(account=12345678, password="password", server="broker_server")
            print("Fetching account details...")
            account_details = self.fetch_account_details()
            print(f"Account details: {account_details}")
            print("Selecting symbol...")
            self.select_symbol("EURUSD")
            print("Fetching tick info...")
            tick_info = self.fetch_tick_info("EURUSD")
            print(f"Tick info: {tick_info}")
        except Exception as e:
            self.log_trade(f"Error: {str(e)}")

if __name__ == "__main__":
    trade_bot = Trade()
    trade_bot.main()
