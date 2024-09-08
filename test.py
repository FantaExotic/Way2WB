import yfinance as yf

class Tickwrapper:
    def __init__(self):
        self.ticker = yf.Ticker("EURUSD=X")
        self.tickerhistory = self.ticker.history(period="1d", interval="1m",prepost=True)#

    def convertcurrency(self):
        self.tickerhistory = self.tickerhistory * 1.2

    def add_to_tickwrappers(self,tickerwrappers):
        tickerwrappers.append(self.tickerhistory)


tickwrappers = list()
tickwrapper = Tickwrapper()

tickwrapper.convertcurrency()
tickwrapper.add_to_tickwrappers(tickwrappers)

print("done")