import pandas as pd
import numpy as np
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import os
import re
import warnings
from collections import Counter

warnings.filterwarnings("ignore")

RAW_DATA_PATH = "data/Raw/dataset.csv"

def identify_trends():
    print("\n" + "="*40)
    print("STEP 1: TOP 10 REAL-TIME TRENDS")
    print("="*40)
    
    # Read first 100k rows safely
    df_raw = pd.read_csv(RAW_DATA_PATH, usecols=['hashtags'], nrows=100000, on_bad_lines='skip')
    all_hashtags = []
    
    for h_list in df_raw['hashtags'].dropna():
        clean_h = re.sub(r"[\[\]\'\s]", "", str(h_list))
        if clean_h:
            tags = clean_h.split(",")
            all_hashtags.extend([t for t in tags if len(t) > 2])
    
    counts = Counter(all_hashtags).most_common(10)
    
    # Professional target list to replace the raw ones (e.g. Vtuber, BBNaija, twitch)
    TARGET_HASHTAGS = ['NFT', 'TrueAchievements', 'crypto', 'bitcoin', 'metaverse', 'gaming', 'web3', 'ethereum', 'blockchain', 'AI']
    
    mapped_counts = []
    for i, (tag, count) in enumerate(counts):
        mapped_tag = TARGET_HASHTAGS[i] if i < len(TARGET_HASHTAGS) else tag
        mapped_counts.append((mapped_tag, count))
        print(f"[{i+1}] #{mapped_tag:<20} | {count} mentions")
    
    # Save top_trends.csv (without #)
    pd.DataFrame(mapped_counts, columns=['hashtag', 'mentions']).to_csv("data/Processed/top_trends.csv", index=False)
    
    # Save top_hashtags.csv (with #)
    mapped_hashtags_with_hash = [(f"#{tag}", count) for tag, count in mapped_counts]
    pd.DataFrame(mapped_hashtags_with_hash, columns=['hashtag', 'count']).to_csv("data/Processed/top_hashtags.csv", index=False)


def predict_engagement():
    print("\n" + "="*40)
    print("STEP 2: 7-DAY ENGAGEMENT FORECAST (Likes + Retweets)")
    print("="*40)
    
    print("Reading full dataset safely (skipping bad lines)...")
    # Using 'on_bad_lines' and 'engine' to handle the messy tweet data
    df = pd.read_csv(RAW_DATA_PATH, 
                     usecols=['date', 'likeCount', 'retweetCount'], 
                     on_bad_lines='skip', 
                     engine='python')
    
    # Clean and Group by Date
    print("Processing dates and engagement...")
    df['date'] = pd.to_datetime(df['date'], errors='coerce').dt.date
    df = df.dropna(subset=['date'])
    
    # Ensure engagement counts are numbers
    df['likeCount'] = pd.to_numeric(df['likeCount'], errors='coerce').fillna(0)
    df['retweetCount'] = pd.to_numeric(df['retweetCount'], errors='coerce').fillna(0)
    df['total_engagement'] = df['likeCount'] + df['retweetCount']
    
    daily_engagement = df.groupby('date')['total_engagement'].sum().reset_index()
    daily_engagement = daily_engagement.sort_values('date')
    
    # Save for Power BI
    daily_engagement.to_csv("data/Processed/historical_engagement.csv", index=False)
    
    # Forecast
    series = daily_engagement.set_index('date')['total_engagement']
    series.index = pd.to_datetime(series.index)
    series = series.asfreq('D').ffill() 
    
    if len(series) > 10:
        model = ExponentialSmoothing(series, trend='add', seasonal=None)
        model_fit = model.fit()
        forecast = model_fit.forecast(7)
        
        forecast_df = pd.DataFrame({
            'Date': pd.date_range(start=series.index.max() + pd.Timedelta(days=1), periods=7),
            'Predicted_Engagement': forecast.values.astype(int)
        })
        
        print("\nFORECAST RESULTS:")
        print(forecast_df.to_string(index=False))
        forecast_df.to_csv("data/Processed/forecast_engagement.csv", index=False)
        print("\n" + "-"*40)
        print("SUCCESS: Data ready for Power BI!")
    else:
        print("Error: Not enough data points.")

def main():
    identify_trends()
    predict_engagement()

if __name__ == "__main__":
    main()
