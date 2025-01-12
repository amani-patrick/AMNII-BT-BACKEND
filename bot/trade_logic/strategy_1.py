from bot.trade_logic import fetch_data
from bot.trade_logic.utils import smc_indicators_res
from trade_logic.utils import select_symbol as select
from trade_logic.utils import tick_info,check_dataframe,calculate_tp_sl
import smartmoneyconcepts as smc
import pandas  as pd





def fvg_strategy(fvg_res: pd.DataFrame, current_price_data: dict,symbol,data):
    '''
    :param fvg_res: DataFrame with FVG analysis containing columns ['FVG', 'Top', 'Bottom', 'MitigatedIndex']
    :param current_price_data: Dictionary containing current price data with 'low' price
    '''
    swing_highs_lows_res,fvg_res,ob_res,prev_high_low_res = smc_indicators_res(fetch_data(symbol))

    select(symbol)
    tick_info=tick_info(symbol)
    check_dataframe(current_price_data)
    current_index = fvg_res.index[-1]
    current_row=fvg_res.iloc[-1]

    if pd.isna(current_row['FVG']):
        lookback_data = fvg_res.iloc[-30:-1]
        action_performed = False
        
        for i,prev_row in lookback_data.iterrows():
            if prev_row['MitigatedIndex'] == current_index:
                low_price = current_price_data['low']
                if prev_row['FVG']==-1.0:
                    action='SELL'
                    tp,sl=calculate_tp_sl(action,calculate_tp_sl)
                elif prev_row['FVG']==1.0:
                    action='BUY'
                    tp,sl=calculate_tp_sl(action,calculate_tp_sl)
    return {
        "action": action,
        "tp": tp,
        "sl": sl
    }




    



