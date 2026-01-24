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
JST = timezone(timedelta(hours=9))

def get_detailed_analysis(pattern_name, sentiment):
    """Provides professional technical explanations for detected patterns"""
    name_clean = pattern_name.replace("Bullish ", "").replace("Bearish ", "").strip()
    
    # Professional Technical Descriptions
    library = {
        "Hammer": "A reversal signal showing that sellers tried to push price down but were met with overwhelming buying pressure, leaving a long lower wick.",
        "Engulfing": "A high-conviction reversal pattern where the current candle completely 'swallows' the previous one, indicating a total shift in trend control.",
        "Doji": "A sign of peak market indecision. The open and close are nearly identical, suggesting the current trend is losing steam.",
        "Morningstar": "A classic 3-candle bottom reversal. It signals that the previous downtrend has exhausted and a new uptrend is beginning.",
        "Eveningstar": "A top reversal pattern indicating that the bullish momentum has stopped and sellers are starting to take over.",
        "Shootingstar": "A bearish signal where buyers tried to reach new highs but failed, closing near the open with a long upper wick.",
        "Marubozu": "A 'Bald' candle with no wicks. It shows extreme dominance by one side (buyers or sellers) from the opening to the closing bell.",
        "Harami": "A 'Pregnant' pattern where a small candle stays inside the previous large one, signaling that the current move is losing momentum.",
        "Tweezerbottom": "Two candles with identical lows, showing a very strong support floor that the bears cannot break."
    }
    
    explanation = library.get(name_clean, "A technical formation indicating a localized shift in buyer/seller psychology.")
    return f"{sentiment} {name_clean}: {explanation}"

def get_projection(pattern_name):
    """Bitcoin-specific 'What's Next' logic"""
    name = pattern_name.lower()
    if "bullish" in name:
        return "EXPECTED MOVE: Upward Continuation. Bitcoin is showing strength. Strategy: Look for entry on a 5-minute pullback or a break of the pattern high."
    elif "bearish" in name:
        return "EXPECTED MOVE: Downward Pressure. Risk is high. Strategy: Protect long positions or wait for a lower support level (like the 200 EMA) to be tested."
    elif "doji" in name:
        return "EXPECTED MOVE: Volatile Breakout. Bitcoin is compressing. Strategy: Do not trade inside this range; wait for price to break above or below the Doji's wicks."
    else:
        return "EXPECTED MOVE: Sideways Consolidation. Bitcoin is in a 'wait and see' mode. Strategy: Avoid high leverage; wait for a confirmed pattern."

def analyze_all_patterns(df):
    """Scans the last 5 completed candles to ensure a pattern is found if one exists"""
    df.columns = [x.lower() for x in df.columns]
    patterns_df = df.ta.cdl_pattern(name="all")
    
    if patterns_df is None or patterns_df.empty:
        return "Normal", "Steady BTC movement.", "Maintain watch."

    # SCAN BACK LOGIC: Look at the last 5 candles (starting from the most recent completed one)
    # This ensures we don't just show 'Normal' if a Hammer happened 15 mins ago.
    for i in range(2, 7): 
        target_candle = patterns_df.iloc[-i]
        active = target_candle[target_candle != 0]
        
        if not active.empty:
            found_list = []
            for raw_name, value in active.items():
                clean_name = raw_name.replace('CDL_', '').replace('_', ' ').title()
                sentiment = "Bullish" if value > 0 else "Bearish"
                found_list.append(f"{sentiment} {clean_name}")
            
            main_pattern = found_list[0]
            detailed_exp = get_detailed_analysis(main_pattern, sentiment)
            projection = get_projection(main_pattern)
            
            # Record which candle this was found on
            found_at_idx = i - 1
            return main_pattern, f"(Detected {found_at_idx} candle(s) ago) {detailed_exp}", projection

    return "Normal", "No major technical patterns in the last 5 periods. Price is in standard consolidation.", "Wait for a breakout."

def update_bitcoin_json():
    intervals = {
        "15 Minute": Interval.in_15_minute,
        "30 Minute": Interval.in_30_minute,
        "1 Hour": Interval.in_1_hour
    }
    
    run_time_jst = datetime.now(JST).strftime("%Y-%m-%d %H:%M JST")
    new_entry = {"run_timestamp_jst": run_time_jst, "timeframes": {}}

    for label, tv_interval in intervals.items():
        try:
            df = tv.get_hist(symbol='BTCUSD', exchange='BITSTAMP', interval=tv_interval, n_bars=100)
            if df is not None and not df.empty:
                # Actual data for the latest finished candle
                jst_candle_time = (df.index[-2] + timedelta(hours=9)).strftime("%Y-%m-%d %H:%M JST")
                
                pattern, desc, next_move = analyze_all_patterns(df)
                
                new_entry["timeframes"][label] = {
                    "last_checked_jst": jst_candle_time,
                    "price_current": round(df['close'].iloc[-1], 2),
                    "pattern_found": pattern,
                    "detailed_explanation": desc,
                    "whats_next_prediction": next_move
                }
        except Exception as e:
            print(f"Error: {e}")

    # Unlimited History Save
    history = []
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            try: history = json.load(f)
            except: history = []

    history.append(new_entry)
    with open(file_path, 'w') as f:
        json.dump(history, f, indent=4)
    print(f"Updated BTC Data at {run_time_jst}")

if __name__ == "__main__":
    update_bitcoin_json()
