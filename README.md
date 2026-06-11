# Hyperliquid Trader Sentiment Analysis (Primetrade.ai Data Science Assessment)

This repository contains a data engineering and exploratory data analysis pipeline that correlates **184,263 historical trade execution rows** from Hyperliquid with daily **Bitcoin Fear & Greed Index** classifications. 

The goal of this analysis is to evaluate how macro-market psychology drives retail trader volume, profitability, and win-rate metrics.

## 📊 Core Performance Matrix

| Market Sentiment State | Total Executed Trades | Average Realized PnL ($) | Median PnL ($) | Win Rate (%) |
| :--- | :--- | :--- | :--- | :--- |
| **Extreme Greed** | 6,962 | $25.42 | $0.00 | 49.01% |
| **Greed** | 36,289 | $87.89 | $0.00 | 44.65% |
| **Neutral** | 7,141 | $22.23 | $0.00 | 31.72% |
| **Fear** | 133,871 | $50.05 | $0.00 | 41.51% |

## 💡 Key Alpha Insights
* **The Volatility Cluster (Fear Overdrive):** An overwhelming 72.6% of all trading volume occurs during **Fear** regimes, showing that retail traders aggressively ramp up execution volume during market drawdowns.
* **The Momentum Payout (Greed Efficiency):** While Extreme Greed holds the highest baseline trade win rate (49.01%), the standard **Greed** phase captures the highest average profitability ($87.89/trade). 
* **The Consolidation Trap (The Neutral Danger Zone):** **Neutral** market environments are mathematically the most hazardous for momentum strategies, with win rates plunging to 31.72% due to sideways chop and computational whip-saws.

##  Data Pipeline Architecture
* **High-Volume Scale:** Efficiently streams and maps large-scale 47.3 MB CSV datasets.
* **Temporal Normalization:** Restructured disparate localized Unix epoch milliseconds and irregular string records into ISO standard `YYYY-MM-DD` strings for absolute calendar alignment.

##  How to Run
1. Clone this repository.
2. Ensure your datasets (`hyperliquid_trader_data.csv` and `bitcoin_fear_greed.csv`) are located in your working directory.
3. Execute the pipeline:
```bash
python runner.py




