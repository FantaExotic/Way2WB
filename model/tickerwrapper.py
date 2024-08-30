import yfinance as yf
from utils.helpfunctions import *

class TickerWrapper:

    def __init__(self,ticker: yf.Ticker) -> None:
        self.ticker = ticker
        self.tickerhistory = dict()

    def set_tickerhistory(self, period: str, interval: str):
        self.tickerhistory[interval] = self.ticker.history(period = period, interval = interval, prepost=True)

    def get_tickerhistory(self, period: str):
        interval = setTickerArgs(period)
        return self.tickerhistory[interval]
        
    def verify_tickerhistory_exists(self, period: str) -> bool:
        """Checks if tickerhistory for this period already exists in model.tickerlist"""
        interval = setTickerArgs(period)
        try:
            temp = self.tickerhistory[interval]
            return True
        except:
            #print("Tickerhistory doesnt exist yet in local memory. Will be downloaded now")
            return False

    def verify_period_valid(self, period: str) -> bool:
        if period in self.ticker._price_history._history_metadata['validRanges']:
            return True
        else:
            #print("Period for this ticker is invalid! Shorted period will be used instead.")
            return False
        
    def verify_ticker_valid(self) -> bool:
        """Verifies that the downloaded ticker is a valid one (to prevent empty tickers)"""
        # trailingPegRatio is the best identifier which I found so far, improvable!
        dict_invalid_ticker = {'trailingPegRatio': None}
        if self.ticker.info != dict_invalid_ticker:
            return True
        else:
            print("Tickerinformation invalid. Recheck entered ticker symbol!")
            return False
