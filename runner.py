import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set paths directly
folder_path = r"C:\Users\Admin\desktop\Trader_Sentiment_Analysis"
os.chdir(folder_path)

print("Reading files directly from desktop folder...")
df_trades = pd.read_csv('hyperliquid_trader_data.csv', low_memory=False)
df_sentiment = pd.read_csv('bitcoin_fear_greed.csv', low_memory=False)

print("\n--- Auto-Detecting Column Names ---")
time_col = 'Timestamp'
sent_date_col = 'date'

print(f"Using '{time_col}' for trade timestamps.")
print(f"Using '{sent_date_col}' for sentiment dates.")

print("\nProcessing dates and cleaning data...")

# SMART PARSING: Try parsing numbers as Unix milliseconds, fallback to standard strings if text
try:
    if pd.api.types.is_numeric_dtype(df_trades[time_col]):
        # If timestamps are raw numbers (millisecond Epochs)
        df_trades['trade_date'] = pd.to_datetime(df_trades[time_col], unit='ms', errors='coerce').dt.date.astype(str)
    else:
        # If timestamps are standard date strings
        df_trades['trade_date'] = pd.to_datetime(df_trades[time_col], errors='coerce').dt.date.astype(str)
except Exception:
    # Fail-safe string slice method if everything else fails
    df_trades['trade_date'] = df_trades[time_col].astype(str).str[:10]

# Normalize sentiment file date matching
df_sentiment['trade_date'] = pd.to_datetime(df_sentiment[sent_date_col], errors='coerce').dt.date.astype(str)

# Clean up any bad parsing transformations safely
df_trades = df_trades.dropna(subset=['trade_date'])
df_sentiment = df_sentiment.dropna(subset=['trade_date'])

print(f"Sample trade dates: {df_trades['trade_date'].head(2).tolist()}")
print(f"Sample sentiment dates: {df_sentiment['trade_date'].head(2).tolist()}")

print("Merging dataframes...")
merged_df = pd.merge(df_trades, df_sentiment, on='trade_date', how='inner')

print(f"Merged row count count: {len(merged_df)}")

if len(merged_df) == 0:
    print("\n[WARNING]: Calendar formats still mismatched. Trying aggressive string matching cleaning...")
    # Last ditch absolute fallback cleaning raw strings
    df_trades['trade_date'] = df_trades[time_col].astype(str).str.extract(r'(\d{4}-\d{2}-\d{2})')[0]
    df_sentiment['trade_date'] = df_sentiment[sent_date_col].astype(str).str.extract(r'(\d{4}-\d{2}-\d{2})')[0]
    merged_df = pd.merge(df_trades, df_sentiment, on='trade_date', how='inner')
    print(f"Remerged row count: {len(merged_df)}")

pnl_col = 'Closed PnL'
class_col = 'classification'

if len(merged_df) > 0:
    closed_trades = merged_df.dropna(subset=[pnl_col]).copy()
    closed_trades[pnl_col] = pd.to_numeric(closed_trades[pnl_col], errors='coerce')
    closed_trades['is_win'] = closed_trades[pnl_col] > 0
    acc_col = 'Account' if 'Account' in closed_trades.columns else closed_trades.columns[0]

    print("Calculating metrics...")
    sentiment_summary = closed_trades.groupby(class_col).agg(
        total_trades=(acc_col, 'count'),
        average_pnl=(pnl_col, 'mean'),
        median_pnl=(pnl_col, 'median'),
        win_rate_pct=('is_win', 'mean')
    ).reset_index()

    sentiment_summary['win_rate_pct'] = (sentiment_summary['win_rate_pct'] * 100).round(2)
    sentiment_summary = sentiment_summary.round(2)

    print("\n==============================================")
    print("             ASSIGNMENT RESULTS               ")
    print("==============================================")
    print(sentiment_summary.to_string(index=False))
    print("==============================================")

    # Generate and save chart images directly to the folder
    sns.set_theme(style="whitegrid")
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    sns.barplot(data=sentiment_summary, x=class_col, y='win_rate_pct', palette='viridis', ax=axes[0])
    axes[0].set_title('Win Rate (%) Across Market Sentiment Tiers', fontweight='bold')
    axes[0].axhline(50, color='red', linestyle='--')

    sns.barplot(data=sentiment_summary, x=class_col, y='average_pnl', palette='coolwarm', ax=axes[1])
    axes[1].set_title('Average Realized PnL ($) by Sentiment Category', fontweight='bold')
    axes[1].axhline(0, color='black', linewidth=1)

    plt.tight_layout()
    plt.savefig('final_analysis_plots.png', dpi=150)
    print("\nSuccess! Chart image saved as 'final_analysis_plots.png'")
else:
    print("\nCRITICAL ERR: No matching calendar rows found between datasets.")