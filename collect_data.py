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

def get_projection(pattern_name):
    """
    Heuristic logic to predict the 'What's Next' scenario based 
    on standard technical analysis theory.
    """
    name = pattern_name.lower()
    
    if "bullish" in name:
        return "Bias: Bullish. Expect upward momentum. Watch for a 'Bullish Marubozu' or a break above the current High for confirmation."
    elif "bearish" in name:
        return "Bias: Bearish. Expect downward pressure. Watch for a 'Bearish Marubozu' or a break below the current Low for confirmation."
    elif "doji" in name:
        return "Bias: Neutral/Indecision. The market is at a crossroads. Watch for a high-volume breakout to determine the next trend."
    elif "hammer" in name:
        return "Bias: Potential Reversal. Look for a bullish 'Confirmation Candle' closing above the Hammer's body."
    elif "star" in name:
        return "Bias: Reversal Warning. Significant reversal signal detected. Look for follow-through in the direction of the long shadow."
    elif "harami" in name:
        return "Bias: Consolidation. Volatility is contracting. Watch for a 'Breakout' from the mother candle's range."
    else:
        return "Bias: Consolidation. Standard price action. Watch for new pattern formations or trendline breaks."

def analyze_all_patterns(df):
    """
    Scans for ALL 60+ candlestick patterns and generates 
    explanations and 'What's Next' projections.
    """
    df.columns = [x.lower() for x in df.columns]
    
    # name="all" triggers detection of every pattern in the pandas_ta library
    patterns_df = df.ta.cdl_pattern(name="all")
    
    if patterns_df is None or patterns_df.empty:
        return "Normal", "Steady market movement.", "Maintain watch."

    # Get the results for the most recent candle
    latest_candle = patterns_df.iloc[-1]
    
    # Filter only columns where value is not 0 (100 = Bullish, -100 = Bearish)
    active_patterns = latest_candle[latest_candle != 0]
    
    if active_patterns.empty:
        return "Normal", "No specific candlestick pattern detected.", "Wait for a clear signal."

    found_patterns = []
    for raw_name, value in active_patterns.items():
        clean_name = raw_name.replace('CDL_', '').replace('_', ' ').title()
        sentiment = "Bullish" if value > 0 else "Bearish"
        found_patterns.append(f"{sentiment} {clean_name}")

    # Combine found patterns
    final_pattern_name = ", ".join(found_patterns)
    explanation = f"Detected: {final_pattern_name}."
    
    # Generate 'What's Next' based on the primary (first) detected pattern
    whats_next = get_projection(found_patterns[0])
    
    return final_pattern_name, explanation, whats_next

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
            # Fetch 100 bars to capture complex multi-candle patterns
            df = tv.get_hist(symbol='XAUUSD', exchange='OANDA', interval=tv_interval, n_bars=100)
            
            if df is not None and not df.empty:
                pattern, desc, next_move = analyze_all_patterns(df)
                new_entry["data"][label] = {
                    "price": round(df['close'].iloc[-1], 2),
                    "pattern": pattern,
                    "explanation": desc,
                    "whats_next": next_move
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

    # Check for duplicates to avoid multi-run errors in the same 15min block
    if not any(d.get('timestamp') == timestamp_str for d in full_history):
        full_history.append(new_entry)
        
        with open(file_path, 'w') as f:
            json.dump(full_history, f, indent=4)
        print(f"Successfully updated. Total history size: {len(full_history)} records.")
    else:
        print("Data for this exact timestamp already exists. Skipping.")

if __name__ == "__main__":
    update_json()
