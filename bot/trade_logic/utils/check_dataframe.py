from bot.trade_logic.utils import smc_indicators_res
from bot.trade_logic import fetch_data
from bot.trade_logic.utils import symbol

def check_dataframe(current_price_data):
    
    swing_highs_lows_res,fvg_res,ob_res,prev_high_low_res= smc_indicators_res(fetch_data(symbol))
    required_columns = ['FVG', 'Top', 'Bottom', 'MitigatedIndex']
    for col in required_columns:
        if col not in fvg_res.columns:
            raise ValueError(f"Missing required column: {col}")
    if 'low' not in current_price_data:
            raise ValueError("Current price data must contain a 'low' key.")