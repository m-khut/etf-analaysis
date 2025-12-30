import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("prices.csv", parse_dates=["Date"], index_col=["Date"])

class ETF:
    def __init__(self, name: str, prices: pd.Series):
        self.name = name
        self.prices = prices.sort_index()
        self.returns = self.cal_returns()

    def cal_returns(self) -> pd.Series:
        return self.prices.pct_change().dropna()
    
    def cumulative_returns(self) -> pd.Series:
        return (1+self.returns).cumprod()
    
    def rolling_volatility(self, window: int = 60) -> pd.Series:
        rolling_std = self.returns.rolling(window).std()
        return rolling_std * np.sqrt(252)     #252 = Avg. Market open days in a year
    
    def max_drawdown(self) -> float:
        cum = self.cumulative_returns()
        running_max = cum.cummax()
        drawdown = cum / running_max - 1.0
        return drawdown.min()
    
    def annualized_return(self) -> float:
        mean_daily = self.returns.mean()
        return mean_daily * 252
    
    def annualized_volatility(self) -> float:
        std_daily = self.returns.std()
        return std_daily * np.sqrt(252)
    
spy = ETF("SPY", data["SPY"])
qqq = ETF("QQQ", data["QQQ"])
tlt = ETF("TLT", data["TLT"])
gld = ETF("GLD", data["GLD"])
uso = ETF("USO", data["USO"])

etfs = [spy, qqq, tlt, gld, uso]

def build_risk_table(etfs_list):
    rows = []
    for etf in etfs_list:
        row = {
            "ETF": etf.name,
            "Ann_Return":etf.annualized_return(),
            "Ann_Vol": etf.annualized_volatility(),
            "Max_Drawdown": etf.max_drawdown(),
        }
        rows.append(row)
    
    risk_df = pd.DataFrame(rows).set_index("ETF")
    return risk_df

def plot_rolling_volatility(etfs_list, window: int = 60):
    plt.figure(figsize=(12, 6))
    for etf in etfs_list:
        etf.rolling_volatility(window).plot(label=etf.name)
    plt.title(f"Rolling {window}-Day Annualized Volatility")
    plt.xlabel("Date")
    plt.ylabel("Volatility")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


def plot_drawdowns(etfs_list):
    plt.figure(figsize=(12, 6))
    for etf in etfs_list:
        cum = etf.cumulative_returns()
        running_max = cum.cummax()
        drawdown = cum / running_max - 1.0
        drawdown.plot(label=etf.name)
    plt.title("Drawdown Curves")
    plt.xlabel("Date")
    plt.ylabel("Drawdown")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    risk_table = build_risk_table(etfs)

    display_table = risk_table.copy()
    display_table["Ann_Return"] = (display_table["Ann_Return"] * 100).round(2)
    display_table["Ann_Vol"] = (display_table["Ann_Vol"] * 100).round(2)
    display_table["Max_Drawdown"] = (display_table["Max_Drawdown"] * 100).round(2)

    print("\n===== RISK DASHBOARD SUMMARY =====\n")
    print("Annualized Return (%), Annualized Volatility (%), Max Drawdown (%)\n")
    print(display_table)

    plot_rolling_volatility(etfs, window=60)
    plot_drawdowns(etfs)
