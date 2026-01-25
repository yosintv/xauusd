import json
import os
import re
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

# 2. Initialize TradingView (Guest Mode)
tv = TvDatafeed()

# Define JST Timezone (UTC+9)
JST = timezone(timedelta(hours=9))

def clean_pattern_name(raw_name):
    """Removes technical suffixes like '10 0.1' and 'CDL_' from names"""
    name = raw_name.replace('CDL_', '').replace('_', ' ')
    name = re.sub(r'[\d\.\s]+$', '', name).strip()
    return name.title()

def get_detailed_explanation(pattern_name, sentiment):
    """Professional technical descriptions for patterns"""
    library = {
        "Hammer": "A classic reversal signal. Sellers drove price down, but buyers stepped in to close near the high.",
        "Doji": "Total market indecision. Bulls and Bears are in a stalemate; a breakout is usually imminent.",
        "Engulfing": "A high-conviction reversal. The current candle body completely covers the previous one.",
        "Inside": "Consolidation pattern. Price is staying within the previous candle's range, waiting for a catalyst.",
        "Morningstar": "A powerful 3-candle bottom signal. Suggests the downtrend is over and buyers are taking over.",
        "Eveningstar": "A bearish top signal. Indicates exhaustion among buyers and a likely shift to a downtrend.",
        "Harami": "A sign of a potential trend change. Suggests momentum is slowing down.",
        "Marubozu": "Extreme dominance. No wicks means one side controlled the price from open to close.",
        "Tweezerbottom": "Support floor confirmed. Two candles hitting the same low suggests strong rejection."
    }
    desc = library.get(pattern_name, "A technical formation indicating a localized shift in buyer/seller psychology.")
    return f"{sentiment} {pattern_name}: {desc}"

def get_projection(pattern_name, sentiment):
    """Bitcoin-specific predictive logic"""
    if sentiment == "Bullish":
        return "EXPECTED MOVE: Upward Strength. Strategy: Look for entry on a pullback or break of the pattern high."
    elif sentiment == "Bearish":
        return "EXPECTED MOVE: Downward Pressure. Strategy: Protect long positions; watch for tests of support."
    else:
        return "EXPECTED MOVE: Consolidation. Strategy: Avoid high leverage; wait for a confirmed breakout."

def analyze_all_patterns(df):
    """Scans the last 5 completed candles to ensure signals aren't missed"""
    df.columns = [x.lower() for x in df.columns]
    patterns_df = df.ta.cdl_pattern(name="all")
    
    if patterns_df is None or patterns_df.empty:
        return "Normal", "Steady BTC movement.", "Wait for next candle close."

    for i in range(2, 7): 
        target_candle = patterns_df.iloc[-i]
        active = target_candle[target_candle != 0]
        
        if not active.empty:
            raw_name = active.index[0]
            val = active.iloc[0]
            sentiment = "Bullish" if val > 0 else "Bearish"
            
            clean_name = clean_pattern_name(raw_name)
            explanation = get_detailed_explanation(clean_name, sentiment)
            projection = get_projection(clean_name, sentiment)
            
            return f"{sentiment} {clean_name}", f"(Detected {i-1} candle(s) ago) {explanation}", projection

    return "Normal", "No major patterns in last 5 periods.", "Wait for a breakout."

def update_bitcoin_json():
    intervals = {
        "15 Minute": Interval.in_15_minute,
        "30 Minute": Interval.in_30_minute,
        "45 Minute": Interval.in_45_minute,
        "1 Hour": Interval.in_1_hour
    }
    
    # --- DEDUPLICATION LOGIC ---
    # Round current time to the nearest 5-minute block (e.g., 12:03 becomes 12:00)
    now = datetime.now(JST)
    rounded_minute = (now.minute // 5) * 5
    slot_time = now.replace(minute=rounded_minute, second=0, microsecond=0).strftime("%Y-%m-%d %H:%M JST")
    
    new_entry = {"run_timestamp_jst": slot_time, "timeframes": {}}

    print(f"Fetching Bitcoin data for slot: {slot_time}...")

    for label, tv_interval in intervals.items():
        try:
            df = tv.get_hist(symbol='BTCUSD', exchange='BITSTAMP', interval=tv_interval, n_bars=100)
            
            if df is not None and not df.empty:
                interval_close = float(round(df['close'].iloc[-2], 2))
                live_price = float(round(df['close'].iloc[-1], 2))
                candle_time = (df.index[-2] + timedelta(hours=9)).strftime("%Y-%m-%d %H:%M JST")
                
                pattern, desc, next_move = analyze_all_patterns(df)
                
                new_entry["timeframes"][label] = {
                    "last_closed_candle_jst": candle_time,
                    "interval_close_price": interval_close,
                    "live_market_price": live_price,
                    "pattern_found": pattern,
                    "detailed_explanation": desc,
                    "whats_next_prediction": next_move
                }
        except Exception as e:
            print(f"Error fetching {label}: {e}")

    # History Management
    full_history = []
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            try:
                full_history = json.load(f)
            except json.JSONDecodeError:
                full_history = []

    # Check if this 5-minute slot already exists
    updated = False
    for i, entry in enumerate(full_history):
        if entry.get("run_timestamp_jst") == slot_time:
            full_history[i] = new_entry  # Replace existing data with fresh live prices
            updated = True
            print(f"Updated existing entry for {slot_time}")
            break
    
    if not updated:
        full_history.append(new_entry)
        print(f"Added new entry for {slot_time}")

    # Safety: Keep only the last 1000 entries (~3.5 days of 5-min data)
    if len(full_history) > 1000:
        full_history = full_history[-1000:]
    
    with open(file_path, 'w') as f:
        json.dump(full_history, f, indent=4)
    
    print(f"Done. Total history size: {len(full_history)}")

if __name__ == "__main__":
    update_bitcoin_json()
