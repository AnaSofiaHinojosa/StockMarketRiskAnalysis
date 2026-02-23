import numpy as np
from scipy.stats import norm
from parameters import TIME_HORIZON, Z_SCORE_SAFE, DEFAULT_PROB_THRESHOLD, Z_SCORE_DISTRESS
from financial_data import DataDownloader
import pandas as pd

class Company(DataDownloader):
    def __init__(self, ticker):
        super().__init__(ticker)
        self.balance_sheet = self.get_balance_sheet()
        self.income_statement = self.get_income_statement()
        self.market_data = self.get_market_data()

    def get_total_assets(self):
        return self.balance_sheet["Total Assets"].iloc[0]

    def get_total_liabilities(self):
        return self.balance_sheet["Total Liabilities Net Minority Interest"].iloc[0]

    def get_working_capital(self):
        current_assets = self.balance_sheet["Total Assets"].iloc[0] - self.balance_sheet["Total Non Current Assets"].iloc[0]
        current_liabilities = self.balance_sheet["Current Liabilities"].iloc[0]
        return current_assets - current_liabilities

    def get_retained_earnings(self):
        return self.balance_sheet["Retained Earnings"].iloc[0]

    def get_ebit(self):
        return self.income_statement["EBIT"].iloc[0]

    def get_sales(self):
        return self.income_statement["Total Revenue"].iloc[0]

    def get_market_value_of_equity(self):
        return self.balance_sheet["Stockholders Equity"].iloc[0]

    def get_short_term_debt(self):
        return self.balance_sheet["Current Debt"].iloc[0]

    def get_long_term_debt(self):
        return self.balance_sheet["Long Term Debt"].iloc[0]

    def get_default_point(self):
        # Default point = Current liabilities + 0.5 Long term liabilities
        total_liabilities = self.get_total_liabilities()
        current_liabilities = self.balance_sheet["Current Liabilities"].iloc[0]
        long_term_liabilities = total_liabilities - current_liabilities
        return current_liabilities + 0.5 * long_term_liabilities

    def get_assets(self):
        return self.balance_sheet["Total Assets"].values

class AltmanZScore(Company):
    def __init__(self, ticker):
        super().__init__(ticker)
        self.total_assets = self.get_total_assets()
        self.total_liabilities = self.get_total_liabilities()

    def calculate(self):

        X1 = self.get_working_capital() / self.total_assets
        X2 = self.get_retained_earnings() / self.total_assets
        X3 = self.get_ebit() / self.total_assets
        X4 = self.get_market_value_of_equity() / self.total_liabilities
        X5 = self.get_sales() / self.total_assets

        z_score = 1.2*X1 + 1.4*X2 + 3.3*X3 + 0.6*X4 + 1.0*X5
        return z_score

class MertonModel(Company):
    def __init__(self, ticker):
        super().__init__(ticker)

    def get_asset_return(self):
        # Log returns for total assets
        assets = self.get_assets()
        assets_series = pd.Series(assets)
        returns = np.log(assets_series / assets_series.shift(1)).dropna()
        return returns.mean()
    
    def get_asset_volatility(self):
        assets = self.get_assets()
        assets_series = pd.Series(assets)
        returns = np.log(assets_series / assets_series.shift(1)).dropna()
        return returns.std()
    
    def solve_asset_value_kmv(self, tol=1e-6, max_iter=100):
        E = self.get_market_value_of_equity()
        D = self.get_default_point()
        T = TIME_HORIZON
        r = self.get_asset_return()
        sigma = self.get_asset_volatility()

        # initial guess (book assets)
        V = self.get_total_assets()

        for _ in range(max_iter):
            d1 = (np.log(V / D) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
            d2 = d1 - sigma * np.sqrt(T)

            E_model = V * norm.cdf(d1) - D * np.exp(-r * T) * norm.cdf(d2)

            # Newton-style update
            V_new = V + (E - E_model) / norm.cdf(d1)

            if abs(V_new - V) < tol:
                break
            V = V_new

        return V

    def calculate_default_probability(self):
        V = self.solve_asset_value_kmv()
        D = self.get_default_point()
        T = TIME_HORIZON
        r = self.get_asset_return()
        sigma = self.get_asset_volatility()

        d1 = (np.log(V/D) + (r + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
        d2 = d1 - sigma*np.sqrt(T)

        default_probability = 1 - norm.cdf(d2)
        return default_probability

class CreditDecision:
    def __init__(self, z_score, default_probability):
        self.z_score = z_score
        self.default_probability = default_probability

    def decision(self):
        if self.z_score > Z_SCORE_DISTRESS and self.default_probability < DEFAULT_PROB_THRESHOLD:
            return "APPROVED"

        elif self.z_score > Z_SCORE_SAFE:
            return "APPROVED"

        elif self.z_score <= Z_SCORE_DISTRESS or self.default_probability >= DEFAULT_PROB_THRESHOLD:
            return "DENIED"

        else:
            return "DENIED"