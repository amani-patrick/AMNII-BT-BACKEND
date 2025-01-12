import smartmoneyconcepts as smc
from amnii_bt.bot.trade_logic.utils import smc_indicators_res
from bot.trade_logic import fetch_data
from bot.trade_logic.utils import symbol


def detect_orderBlock(data, swing_highs_lows_res, close_mitigation=False):
    """
    Detect bullish and bearish order blocks using smc.ob method.
    """
    swing_highs_lows_res,fvg_res,ob_res,prev_high_low_res = smc_indicators_res(fetch_data(symbol))
    order_blocks = smc.ob(data, swing_highs_lows_res, close_mitigation)
    order_blocks['OB'] = order_blocks['OB'].apply(lambda x: "Bullish" if x == 1 else "Bearish" if x == -1 else "None")
    
    return order_blocks

def strategy_with_order_blocks(data, swing_highs_lows_res, close_mitigation=False):
    """
    Strategy that uses order blocks to generate trade signals.
    """
    data = data[['open', 'high', 'low', 'close']]  
    order_blocks = detect_orderBlock(data, swing_highs_lows_res, close_mitigation)
    valid_order_blocks = order_blocks.dropna(subset=['OB'])

    # If no valid order blocks are found, hold
    if valid_order_blocks.empty:
        return {"action": "Hold", "tp": None, "sl": None}
    
    # Get the latest valid order block (most recent OB)
    latest_ob = valid_order_blocks.iloc[-1]
    
    action = None
    tp = None
    sl = None

    # If there is a bullish order block
    if latest_ob['OB'] == "Bullish":
        action = "Buy"
        tp = latest_ob['Top']  # Take profit at the top of the order block
        sl = latest_ob['Bottom'] - 0.0001  # Set stop-loss below the bottom of the order block by a small buffer
    
    # If there is a bearish order block
    elif latest_ob['OB'] == "Bearish":
        action = "Sell"
        tp = latest_ob['Bottom']  # Take profit at the bottom of the order block
        sl = latest_ob['Top'] + 0.0001  # Set stop-loss above the top of the order block by a small buffer
    
    else:
        action = "Hold"  # If no valid order block detected
    
    return {
        "action": action,
        "tp": tp,
        "sl": sl
    }

