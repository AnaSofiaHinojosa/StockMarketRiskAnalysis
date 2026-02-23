import yfinance as yf

class DataDownloader:
    def __init__(self, ticker):
        self.ticker = ticker
        self.stock = yf.Ticker(ticker)

    def get_balance_sheet(self):
        return self.stock.balance_sheet.transpose()

    def get_income_statement(self):
        return self.stock.financials.transpose()

    def get_market_data(self):
        info = self.stock.info
        return {
            "market_cap": info.get("marketCap"),
            "total_debt": info.get("totalDebt"),
            "shares_outstanding": info.get("sharesOutstanding"),
            "beta": info.get("beta")
        }
