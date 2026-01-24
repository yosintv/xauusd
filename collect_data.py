import json
import os
import pandas as pd
import pandas_ta as ta
from datetime import datetime, timezone

# Case-sensitive import handling for tvDatafeed
try:
    from tvDatafeed import TvDatafeed, Interval
except ImportError:
    from tvdatafeed import TvDatafeed, Interval

# 1. Setup Data Directory
folder_path = 'data'
file_path = os.path.join(folder_path, 'value.json')
os.makedirs(folder_path, exist_ok=True)

# 2. Initialize TradingView
tv = TvDatafeed()

def analyze_all_patterns(df):
    """Scans for all available candlestick patterns in pandas_ta"""
    # Standardize column names
    df.columns = [x.lower() for x in df.columns]
    
    # This executes all available candlestick pattern recognition functions
    # Returns a DataFrame where each column is a pattern (e.g., CDL_MORNINGSTAR)
    patterns_df = df.ta.cdl_pattern(name="all")
    
    if patterns_df is None or patterns_df.empty:
        return "Normal", "Steady market movement."

    # Get the last row (latest candle)
    latest_candle_patterns = patterns_df.iloc[-1]
    
    # Filter only patterns that were actually detected (value != 0)
    detected = latest_candle_patterns[latest_candle_patterns != 0]
    
    if detected.empty:
        return "Normal", "No specific candlestick pattern detected."

    # Pick the first detected pattern name
    # Clean up the name (e.g., 'CDL_MORNINGSTAR' -> 'Morningstar')
    raw_name = detected.index[0]
    pattern_name = raw_name.replace('CDL_', '').replace('_', ' ').title()
    
    # Determine direction based on value (positive = bullish, negative = bearish)
    direction = "Bullish" if detected.iloc[0] > 0 else "Bearish"
    full_name = f"{direction} {pattern_name}"
    
    explanation = f"A {direction} {pattern_name} pattern was detected, suggesting a potential {direction.lower()} move."
    
    return full_name, explanation

def update_json():
    intervals = {
        "15m": Interval.in_15_minute,
        "30m": Interval.in_30_minute,
        "45m": Interval.in_45_minute,
        "1h": Interval.in_1_hour
    }
    
    now = datetime.now(timezone.utc)
    timestamp_str = now.strftime("%Y-%m-%d %H:%M %z")
    new_entry = {"timestamp": timestamp_str, "data": {}}

    print(f"Fetching data for {timestamp_str}...")

    for label, tv_interval in intervals.items():
        try:
            df = tv.get_hist(symbol='XAUUSD', exchange='OANDA', interval=tv_interval, n_bars=100)
            if df is not None and not df.empty:
                pattern, desc = analyze_all_patterns(df)
                new_entry["data"][label] = {
                    "price": round(df['close'].iloc[-1], 2),
                    "pattern": pattern,
                    "explanation": desc
                }
        except Exception as e:
            print(f"Error fetching {label}: {e}")

    # 3. Load and Append (Unlimited)
    full_history = []
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            try:
                full_history = json.load(f)
            except:
                full_history = []

    # Prevent duplicates
    if not any(d.get('timestamp') == timestamp_str for d in full_history):
        full_history.append(new_entry)
        with open(file_path, 'w') as f:
            json.dump(full_history, f, indent=4)
        print(f"Saved. Total records: {len(full_history)}")

if __name__ == "__main__":
    update_json()
