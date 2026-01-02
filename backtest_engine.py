import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("prices.csv", parse_dates=["Date"], index_col='Date')

class ETF:
    def __init__(self, name: str, prices: pd.Series):
        self.name = name
        self.prices = prices.sort_index()
        self.returns = self.cal_returns()

    def cal_returns(self):
        return self.prices.pct_change().dropna()
    
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

    def generate_signal(self, window: int=50):

        ma = self.moving_average(window)
        signals = (self.prices > ma).astype(int)
        return signals
    
def backtest_ma_strategy(etf: ETF, window: int = 50):
        rets = etf.returns

        signals = etf.generate_signal(window)
        
        signals = signals.reindex(rets.index).fillna(0)
        position = signals.shift(1).fillna(0)

        strat_rets = rets * position

        bh_cum = (1+rets).cumprod()

        strat_cum = (1+strat_rets).cumprod()

        out = pd.DataFrame({
             "Price": etf.prices.reindex(rets.index),
             "Returns": rets,
             "Position": position,
             "BH_Cum": bh_cum,
             "Strat_Cum": strat_cum,
        })

        return out

def plot_equity_curves(result_df: pd.DataFrame, name: str, window: int = 50):
    plt.figure(figsize=(12, 6))
    result_df["BH_Cum"].plot(label=f"{name} Buy & Hold")
    result_df["Strat_Cum"].plot(label=f"{name} MA{window} Strategy")

    plt.title(f"{name} – Buy & Hold vs {window}-Day MA Strategy")
    plt.xlabel("Date")
    plt.ylabel("Growth of $1")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.axhline(y=1, color='black', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    symbol = input("Insert ticker: ") #SPY, QQQ, TLT, GLD, USO

    if symbol not in data.columns:
        raise ValueError(f"{symbol} not found in prices.csv columns")

    etf = ETF(symbol, data[symbol])

    etf.plot_ma(window=50)

    result = backtest_ma_strategy(etf, window = 50)

    print("\nFirst few rows of backtest result:")
    print(result.head())

    plot_equity_curves(result, etf.name, window=50)
