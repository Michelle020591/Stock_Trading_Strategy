'''
衡量投資組合風險的方式
1. 股價最大回檔(Max Drawdown)
2. VaR(Value at Risk)
(1) Historical VaR
(2) Conditional VaR (CVaR)
(3) Parameter VaR
(4) Monte Calo VaR

'''

import yfinance as yf
import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt


# 下載股票數據
def get_stock_data(ticker, start="2020-01-01", end="2024-01-01"):
    df = yf.download(ticker, start=start, end=end)
    return df

# 取得歷史VaR
def get_historical_VaR(acc_return, percentage=95):
    assert len(acc_return.shape)==1
    VaR = np.percentile(acc_return, 100-percentage)
    sorted_rets = acc_return.sort_values()
    return VaR

# VaR = get_historical_VaR(portfolio_dd['ret_portf'], pct=99)


######### 可修改參數
ticker = "AAPL"             # 股票代號
start_date = "2020-01-01"   # 回測起始時間
end_date = "2024-01-01"     # 回測終止時間
#########
stock_data = get_stock_data(ticker, start="2020-01-01", end="2024-01-01")
stock_data["pct_change"] = stock_data["Close"].pct_change()
print(stock_data)
close_price = stock_data["Close"].iloc[:, 0]
