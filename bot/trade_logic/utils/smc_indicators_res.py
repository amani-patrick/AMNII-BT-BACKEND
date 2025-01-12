import smartmoneyconcepts as smc

def smc_indicators_res(data):
    fvg_res = smc.fvg(data[['open', 'high', 'low', 'close', 'volume']], join_consecutive=False)
    swing_highs_lows_res = smc.swing_highs_lows(data[['open', 'high', 'low', 'close', 'volume']], swing_length=20)
    ob_res = smc.ob(data[['open', 'high', 'low', 'close', 'volume']], swing_highs_lows_res, close_mitigation=False)
    prev_high_low_res = smc.previous_high_low(data[['open', 'high', 'low', 'close', 'volume']], time_frame="1h")   

    return swing_highs_lows_res,fvg_res,ob_res,prev_high_low_res 
