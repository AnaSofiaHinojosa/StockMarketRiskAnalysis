# StockMarketRiskAnalysis

This project is a Python-based credit risk analysis system. It evaluates companies’ credit risk by calculating the **Altman Z-Score** and estimating default probabilities using the **Merton (KMV) model**, then makes a credit decision based on these results.

## Features

- Downloads financial data for a given stock ticker.
- Computes key risk metrics with Altman Z-Score and Merton default probability models.
- Outputs a simple credit approval decision.
- Includes a dashboard for interactive visualization of results.

## How to Run

### 1. Run `main.py`

This script analyzes a predefined list of companies and prints a summary table with Z-Scores, default probabilities, and credit decisions.

'''
python main.py
'''

It will:
- Fetch financial data for tickers like `MSFT`, `AAPL`, `WMT`.
- Calculate both risk metrics.
- Print results in the console.

### 2. Run `dashboard.py`

This script starts an interactive Streamlit dashboard where you can enter stock tickers and see visual results.

1. Install Streamlit if needed:

'''
pip install streamlit
'''

2. Run the dashboard:

'''
streamlit run dashboard.py
'''

3. Open the browser window and enter one or more comma-separated tickers (e.g., `AAPL, MSFT`) to see:
- A table summarizing each company’s risk metrics.
- Charts comparing Z-Scores and default probabilities.
- Visual badges for credit decisions.

## Requirements

- Python 3.7+
- pandas
- numpy
- streamlit
- yfinance
- matplotlib