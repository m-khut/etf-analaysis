import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("prices.csv", parse_dates=["Date"], index_col=["Date"])

class ETF:
    def __init__(self, name: str, prices: pd.Series):
        self.name = name
        self.prices = prices.sort_index()
        self.returns = self.cal_returnes()

    def cal_returns(self) -> pd.Series:
        return self.prices.pct_change().dropna()
    
    def cumulative_returns(self) -> pd.Series:
        return (1+self.returns).cumprod()
    
    def rolling_volatility(self, window: int = 60) -> pd.Series:
        rolling_std = self.returns.rolling(window).std()
        return rolling_std * np.sqrt(252)
    
    