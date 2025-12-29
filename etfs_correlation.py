import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("prices.csv", parse_dates=["Date"], index_col='Date')

class ETF:
    def __init__(self, name, prices):
        self.name = name
        self.prices = prices.sort_index()
        self.returns = self.cal_returns()

    def cal_returns(self):
        return self.prices.pct_change().dropna()
    
spy = ETF("SPY", data['SPY'])
qqq = ETF("QQQ", data['QQQ'])
tlt = ETF("TLT", data['TLT'])
gld = ETF("GLD", data['GLD'])
uso = ETF("USO", data['USO'])

etfs = [spy, qqq, tlt, gld, uso]

# print(spy.returns.head())
# print(qqq.returns.head())
# print(tlt.returns.head())
# print(gld.returns.head())
# print(uso.returns.head())

class Portfolio:
    def __init__(self, etfs):
        self.etfs = etfs

    def portfolio_returns(self, weights=None):
        returns_df = pd.DataFrame({etf.name:etf.returns for etf in self.etfs})

        if weights is None:
            weights = np.ones(len(self.etfs)) / len(self.etfs)

        pf_returns = returns_df.dot(weights)
        return pf_returns
    
    def correlation_matrix(self):
        returns_df = pd.DataFrame({etf.name: etf.returns for etf in self.etfs})
        return returns_df.corr()
    
    def plot_prices(self, figsize=(12,6)):
        for etf in self.etfs:
            etf.prices.plot(label=etf.name)
        plt.title("ETF Prices")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.axhline(y=1, color='black', linestyle='--', alpha=0.5)
        plt.tight_layout()
        plt.show()

    def plot_cumulative_returns(self, figsize=(12,6)):
        for etf in self.etfs:
            (1 + etf.returns).cumprod().plot(label=etf.name)
        plt.title("Cumulative Returns")
        plt.xlabel("Date")
        plt.ylabel("Cumulative Return")
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.axhline(y=1, color='black', linestyle='--', alpha=0.5)
        plt.tight_layout()
        plt.show()

portfolio = Portfolio(etfs)

portfolio_ret = portfolio.portfolio_returns()
print(portfolio_ret.head())

print(portfolio.correlation_matrix())

portfolio.plot_prices()

portfolio.plot_cumulative_returns()
