import json
import os
import pandas as pd
import pandas_ta as ta
from datetime import datetime, timezone, timedelta

# Handle case-sensitivity in the tvDatafeed library
try:
    from tvDatafeed import TvDatafeed, Interval
except ImportError:
    from tvdatafeed import TvDatafeed, Interval

# 1. Setup Data Directory
folder_path = 'data'
file_path = os.path.join(folder_path, 'bitcoin.json')
os.makedirs(folder_path, exist_ok=True)

# 2. Initialize TradingView
tv = TvDatafeed()

# Define JST Timezone (UTC+9)
JST = timezone(timedelta(hours=9))

def get_projection(pattern_name):
    """Predictive logic for Bitcoin price action"""
    name = pattern_name.lower()
    if "bullish" in name:
        return "Bias: Bullish. Bitcoin showing strength. Expect upward continuation; look for a break above the recent high."
    elif "bearish" in name:
        return "Bias: Bearish. Caution required. Expect downward pressure; watch for support levels to hold."
    elif "doji" in name:
        return "Bias: Neutral. Indecision in the crypto market. High volatility usually follows this candle."
    elif "hammer" in name:
        return "Bias: Reversal. Potential bottoming signal. Look for a bullish confirmation candle next."
    else:
        return "Bias: Consolidation. Standard BTC movement. Watch for a breakout of the current range."

def analyze_all_patterns(df):
    """Scans for 60+ patterns on the LAST COMPLETED candle"""
    df.columns = [x.lower() for x in df.columns]
    patterns_df = df.ta.cdl_pattern(name="all")
    
    if patterns_df is None or patterns_df.empty:
        return "Normal", "Steady BTC movement.", "Wait for next candle close."

    # Look at the SECOND to last candle (index -2) because the last one (index -1) is still LIVE
    completed_candle = patterns_df.iloc[-2] 
    
    active_patterns = completed_candle[completed_candle != 0]
    
    if active_patterns.empty:
        return "Normal", "No specific BTC pattern detected on the last completed candle.", "Wait for a clear signal."

    found_list = []
    for raw_name, value in active_patterns.items():
        clean_name = raw_name.replace('CDL_', '').replace('_', ' ').title()
        sentiment = "Bullish" if value > 0 else "Bearish"
        found_list.append(f"{sentiment} {clean_name}")

    final_name = ", ".join(found_list)
    explanation = f"Confirmed {final_name} detected."
    projection = get_projection(found_list[0])
    
    return final_name, explanation, projection

def update_bitcoin_json():
    intervals = {
        "15 Minute": Interval.in_15_minute,
        "30 Minute": Interval.in_30_minute,
        "45 Minute": Interval.in_45_minute,
        "1 Hour": Interval.in_1_hour
    }
    
    # Current Run-time in JST
    run_time_jst = datetime.now(JST).strftime("%Y-%m-%d %H:%M JST")
    new_entry = {"run_timestamp_jst": run_time_jst, "timeframes": {}}

    print(f"Analyzing Bitcoin (BTC/USD) - JST Time: {run_time_jst}...")

    for label, tv_interval in intervals.items():
        try:
            df = tv.get_hist(symbol='BTCUSD', exchange='BITSTAMP', interval=tv_interval, n_bars=100)
            
            if df is not None and not df.empty:
                # Convert the candle index to JST
                # TradingView data is usually UTC; we add 9 hours
                last_completed_index = df.index[-2] # Reference the completed candle
                jst_candle_time = (last_completed_index + timedelta(hours=9)).strftime("%Y-%m-%d %H:%M JST")
                
                pattern, desc, next_move = analyze_all_patterns(df)
                
                new_entry["timeframes"][label] = {
                    "last_completed_candle_jst": jst_candle_time,
                    "price_at_close": round(df['close'].iloc[-2], 2), # Price of the completed candle
                    "current_live_price": round(df['close'].iloc[-1], 2),
                    "pattern": pattern,
                    "explanation": desc,
                    "whats_next": next_move
                }
        except Exception as e:
            print(f"Error fetching Bitcoin {label}: {e}")

    # Load and Append (Unlimited)
    full_history = []
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            try:
                full_history = json.load(f)
            except:
                full_history = []

    full_history.append(new_entry)
    with open(file_path, 'w') as f:
        json.dump(full_history, f, indent=4)
    print(f"Bitcoin history updated. Total records: {len(full_history)}")

if __name__ == "__main__":
    update_bitcoin_json()
