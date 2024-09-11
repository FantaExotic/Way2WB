import yfinance as yf
import time
from datetime import datetime

ticker = yf.Ticker(ticker="AAPL")
tickerhistory_2y = ticker.history(period="2y", interval="1h",prepost=True)
len_tickerhistory_1y = len(tickerhistory_2y) // 2

tickerhistory_1y = tickerhistory_2y.iloc[len_tickerhistory_1y:]

timestampfirsttrade = 345479400
timestamptoday = int(time.time())
print(datetime.fromtimestamp(timestampfirsttrade))
print(datetime.fromtimestamp(timestamptoday))
print("done")