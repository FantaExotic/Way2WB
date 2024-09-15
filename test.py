import yfinance as yf

ticker = yf.Ticker("VOW3.DE")
tickerhistory = ticker.history(period="max")
tickerhistory_adjust = ticker.history(period="max",auto_adjust=False)

print(tickerhistory.index[5800])
print(tickerhistory_adjust.index[5800])
print(tickerhistory["Close"][5800])
print(tickerhistory["Open"][5800])
print(tickerhistory_adjust["Close"][5800])
print(tickerhistory_adjust["Open"][5800])

print("done")