'''
以均線策略回測歷史股票數據
＊ 黃金交叉(Golden Cross)：短均線由下往上穿過長均線，代表看漲的交易訊號，適合買入
＊ 死亡交叉(Death Cross)：短均線由上往下穿過長均線，代表看跌的交易訊號，適合賣出
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

# 計算移動平均線
def calculate_moving_averages(df, short_frame, long_frame):
    df[short] = df["Close"].rolling(window=short_frame).mean()  # 短期均線
    df[long] = df["Close"].rolling(window=long_frame).mean()  # 長期均線
    return df

# 交易策略：均線交叉策略
def apply_trading_strategy(df):
    df["Signal"] = 0
    df.loc[df[short] > df[long], "Signal"] = 1      # 短期均線高於長期均線，買入
    df.loc[df[short] < df[long], "Signal"] = -1     # 短期均線低於長期均線，賣出
    df["Position"] = df["Signal"].diff()            # 記錄交叉點的買賣訊號
    return df

# 回測交易績效
def backtest_strategy(df, initial_capital):
    capital = initial_capital
    shares = 0
    trade_log = []

    for i in range(len(df)):
        close_price = df.iloc[i]["Close"].item()
        if df["Position"].iloc[i] == 2:     # 買入
            shares = capital // close_price
            capital -= shares * close_price
            trade_log.append((df.index[i], "BUY", close_price, capital, shares))

        elif df["Position"].iloc[i] == -2:  # 賣出
            capital += shares * close_price
            trade_log.append((df.index[i], "SELL", close_price, capital, shares))
            shares = 0  # 清倉
    
    # 計算最終資產
    end_close_price = df.iloc[-1]["Close"].item()
    final_value = capital + (shares * end_close_price)
    return trade_log, final_value

# 繪製交易策略圖
def plot_trading_strategy(df, ticker):
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df["Close"], label="Stock Price", color="black", alpha=0.7)
    plt.plot(df.index, df[short], label=short, color="blue", linestyle="dashed")
    plt.plot(df.index, df[long], label=long, color="red", linestyle="dashed")

    buy_signals = df[df["Position"] == 2]
    sell_signals = df[df["Position"] == -2]

    plt.scatter(buy_signals.index, buy_signals["Close"], label="Buy Signal", marker="^", color="green", alpha=1)
    plt.scatter(sell_signals.index, sell_signals["Close"], label="Sell Signal", marker="v", color="red", alpha=1)

    plt.title(f"Stock Trading Strategy for {ticker}")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.show()


# 主程式
# if __name__ == "__main__":

######### 可修改參數
ticker = "AAPL"             # 股票代號
start_date = "2020-01-01"   # 回測起始時間
end_date = "2024-01-01"     # 回測終止時間
short_frame = 5             # 日移動平均，作短期均線
long_frame = 20             # 日移動平均，作長期均線
initial_capital = 10000     # 初始資產
#########

short = "MA" + str(short_frame)
long = "MA" + str(long_frame)
# 處理歷史股價
stock_data = get_stock_data(ticker, start_date, end_date)
stock_data = calculate_moving_averages(stock_data, short_frame, long_frame)
stock_data = apply_trading_strategy(stock_data)
# 紀錄買入／賣出訊號
current_dir = os.getcwd()
stock_data.to_excel(f'{current_dir}/MA/stock_data1.xlsx')
# 回測交易績效
trade_log, final_value = backtest_strategy(stock_data, initial_capital)

print(f"Initial Capital: $10,000")
print(f"Final Portfolio Value: ${final_value}")
print(f"Total Return: {((final_value - initial_capital) / initial_capital) * 100}%")

# 顯示交易紀錄
for trade in trade_log:
    print(f"{trade[0]} - {trade[1]} at ${trade[2]}, Capital: ${trade[3]}, Shares: {trade[4]}")

# 畫出交易圖表
plot_trading_strategy(stock_data, ticker)



