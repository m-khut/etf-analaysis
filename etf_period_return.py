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
    
    def annual_returns(self):
        gross_returns = 1 + self.returns
        annual = gross_returns.groupby(gross_returns.index.year).prod()-1
        return annual
    
    def monthly_returns(self):
        gross_returns = 1 + self.returns
        monthly = gross_returns.resample('M').prod()-1
        return monthly
    
spy = ETF("SPY", data['SPY'])
qqq = ETF("QQQ", data['QQQ'])
tlt = ETF("TLT", data['TLT'])
gld = ETF("GLD", data['GLD'])
uso = ETF("USO", data['USO'])

etfs = [spy, qqq, tlt, gld, uso]

period = input("Enter the monthy / annual return: ")

if period == "Annual":
    print(spy.annual_returns())
    print(qqq.annual_returns())
    print(tlt.annual_returns())
    print(gld.annual_returns())
    print(uso.annual_returns())
else:
    print(spy.monthly_returns())
    print(qqq.monthly_returns())
    print(tlt.monthly_returns())
    print(gld.monthly_returns())
    print(uso.monthly_returns())
