from financial_data import DataDownloader
from models import Company
from models import AltmanZScore
from models import MertonModel
from models import CreditDecision
import pandas as pd

def analyze_company(ticker):

    z_model = AltmanZScore(ticker)
    z_score = z_model.calculate()

    merton = MertonModel(ticker)
    default_prob = merton.calculate_default_probability()

    decision = CreditDecision(z_score, default_prob).decision()

    return {
        "Ticker": ticker,
        "Z-Score": z_score,
        "Default Probability": default_prob,
        "Credit Decision": decision
    }

if __name__ == "__main__":

    tickers = ["MSFT", "AAPL", "WMT"]

    results = []
    for ticker in tickers:
        results.append(analyze_company(ticker))
    
    dataframe = pd.DataFrame(results)
    print(dataframe)
