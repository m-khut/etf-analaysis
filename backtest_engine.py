import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("prices.csv", parse_dates=["Date"], index_col='Date')

class ETF:
    def __init__(self, name: str, prices: pd.Series):
        self.name = name
        self.prices = prices.sort_index()

    def moving_average(self, window: int = 50):
        return self.prices.rolling(window).mean()
    
    def plot_ma(self, window: int =50):
        ma = self.moving_average(window)

        plt.figure(figsize=(12,6))
        self.prices.plot(label = f"{self.name} Price")
        ma.plot(label = f"{self.name} {window}-Day MA")

        plt.title(f"{self.name} Prices vs. {window}-Day Moving Average")
        plt.xlabel("Date")
        plt.ylabel("Prices")
        plt.legend()
        plt.grid(True, alpha = 0.3)
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    symbol = input("Insert ticker: ") #SPY, QQQ, TLT, GLD, USO

    etf = ETF(symbol, data[symbol])

    etf.plot_ma(window=50)