import json
import os
import pandas as pd
import pandas_ta as ta
from datetime import datetime, timezone

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

def get_projection(pattern_name):
    """Predictive logic for Bitcoin price action"""
    name = pattern_name.lower()
    if "bullish" in name:
        return "Bias: Bullish. Bitcoin showing strength. Watch for a breakout above local resistance."
    elif "bearish" in name:
        return "Bias: Bearish. Caution required. Look for support levels to hold."
    elif "doji" in name:
        return "Bias: Neutral. Indecision in the crypto market. High volatility expected."
    elif "hammer" in name:
        return "Bias: Reversal. Potential bottoming signal. Look for high volume confirmation."
    else:
        return "Bias: Consolidation. Standard BTC sideways movement."

def analyze_all_patterns(df):
    """Scans for all 60+ patterns on Bitcoin"""
    df.columns = [x.lower() for x in df.columns]
    patterns_df = df.ta.cdl_pattern(name="all")
    
    if patterns_df is None or patterns_df.empty:
        return "Normal", "Steady BTC movement.", "Maintain watch."

    latest_candle = patterns_df.iloc[-1]
    active_patterns = latest_candle[latest_candle != 0]
    
    if active_patterns.empty:
        return "Normal", "No specific BTC pattern detected.", "Wait for a clear signal."

    found_list = []
    for raw_name, value in active_patterns.items():
        clean_name = raw_name.replace('CDL_', '').replace('_', ' ').title()
        sentiment = "Bullish" if value > 0 else "Bearish"
        found_list.append(f"{sentiment} {clean_name}")

    final_name = ", ".join(found_list)
    projection = get_projection(found_list[0])
    
    return final_name, f"Detected: {final_name}.", projection

def update_bitcoin_json():
    intervals = {
        "15 Minute": Interval.in_15_minute,
        "30 Minute": Interval.in_30_minute,
        "45 Minute": Interval.in_45_minute,
        "1 Hour": Interval.in_1_hour
    }
    
    # Run-time of the script
    run_time = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M %z")
    new_entry = {"run_timestamp": run_time, "timeframes": {}}

    print(f"Analyzing Bitcoin (BTC/USD) - Run Time: {run_time}...")

    for label, tv_interval in intervals.items():
        try:
            df = tv.get_hist(symbol='BTCUSD', exchange='BITSTAMP', interval=tv_interval, n_bars=100)
            
            if df is not None and not df.empty:
                # GET THE ACTUAL CANDLE TIME FROM DATAFRAME INDEX
                candle_time = df.index[-1].strftime("%Y-%m-%d %H:%M")
                
                pattern, desc, next_move = analyze_all_patterns(df)
                
                # STORE USING THE SPECIFIC CANDLE TIME AS THE KEY
                new_entry["timeframes"][label] = {
                    "candle_detected_at": candle_time,
                    "price": round(df['close'].iloc[-1], 2),
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

    # Save to history
    full_history.append(new_entry)
    with open(file_path, 'w') as f:
        json.dump(full_history, f, indent=4)
    print(f"Bitcoin history updated. Total records: {len(full_history)}")

if __name__ == "__main__":
    update_bitcoin_json()
