import yfinance as yf
from helpfunctions import *

class TickerWrapper:

    def __init__(self,ticker: yf.Ticker) -> None:
        self.ticker = ticker
        self.tickerhistory = dict()
        #TODO: add liveticker here!

    def setTickerHistory(self, period: str):
        interval = setTickerArgs(period)
        self.tickerhistory[interval] = self.ticker.history(period = period, interval = interval, prepost=True)

    def getTickerHistory(self, period: str):
        interval = setTickerArgs(period)
        return self.tickerhistory[interval]
        
    def checkTickerHistory(self, period: str) -> bool:
        interval = setTickerArgs(period)
        try:
            ret = self.tickerhistory[interval]
            return True
        except:
            print("no tickerhistory found for this symbol!")
            return False

    def getTicker(self) -> yf.Ticker:
        return self.ticker
