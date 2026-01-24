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
file_path = os.path.join(folder_path, 'value.json')
os.makedirs(folder_path, exist_ok=True)

# 2. Initialize TradingView (Guest Mode)
tv = TvDatafeed()

def analyze_all_patterns(df):
    """
    Scans for ALL 60+ available candlestick patterns.
    If multiple patterns exist on the same candle, it lists them all.
    """
    df.columns = [x.lower() for x in df.columns]
    
    # name="all" triggers detection of every pattern in the pandas_ta library
    patterns_df = df.ta.cdl_pattern(name="all")
    
    if patterns_df is None or patterns_df.empty:
        return "Normal", "Steady market movement."

    # Get the results for the most recent candle
    latest_candle = patterns_df.iloc[-1]
    
    # Filter only columns where value is not 0 (100 for Bullish, -100 for Bearish)
    active_patterns = latest_candle[latest_candle != 0]
    
    if active_patterns.empty:
        return "Normal", "No specific candlestick pattern detected."

    found_patterns = []
    for raw_name, value in active_patterns.items():
        # Clean name: 'CDL_MORNINGSTAR' -> 'Morningstar'
        clean_name = raw_name.replace('CDL_', '').replace('_', ' ').title()
        sentiment = "Bullish" if value > 0 else "Bearish"
        found_patterns.append(f"{sentiment} {clean_name}")

    # Combine all found patterns into one string
    final_name = ", ".join(found_patterns)
    explanation = f"Detected: {final_name}. This suggests a potential {sentiment.lower()} bias."
    
    return final_name, explanation

def update_json():
    intervals = {
        "15m": Interval.in_15_minute,
        "30m": Interval.in_30_minute,
        "45m": Interval.in_45_minute,
        "1h": Interval.in_1_hour
    }
    
    # Capture current UTC time with timezone offset
    now = datetime.now(timezone.utc)
    timestamp_str = now.strftime("%Y-%m-%d %H:%M %z")
    new_entry = {"timestamp": timestamp_str, "data": {}}

    print(f"Fetching XAUUSD data for {timestamp_str}...")

    for label, tv_interval in intervals.items():
        try:
            # Fetch 100 bars to ensure complex patterns (like Three White Soldiers) are detectable
            df = tv.get_hist(symbol='XAUUSD', exchange='OANDA', interval=tv_interval, n_bars=100)
            
            if df is not None and not df.empty:
                pattern, desc = analyze_all_patterns(df)
                new_entry["data"][label] = {
                    "price": round(df['close'].iloc[-1], 2),
                    "pattern": pattern,
                    "explanation": desc
                }
            else:
                print(f"Warning: No data for {label}")
        except Exception as e:
            print(f"Error fetching {label}: {e}")

    # 3. Load, Append (Unlimited), and Save
    full_history = []
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            try:
                full_history = json.load(f)
            except json.JSONDecodeError:
                full_history = []

    # Prevent duplicate records for the exact same timestamp
    if not any(d.get('timestamp') == timestamp_str for d in full_history):
        full_history.append(new_entry)
        
        with open(file_path, 'w') as f:
            json.dump(full_history, f, indent=4)
        print(f"Update complete. Total records in history: {len(full_history)}")
    else:
        print("Data for this timestamp already exists. Skipping.")

if __name__ == "__main__":
    update_json()
