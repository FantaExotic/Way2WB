import yfinance as yf
from utils.helpfunctions import *

class TickerWrapper:

    def __init__(self,ticker: yf.Ticker) -> None:
        self.ticker = ticker
        self.tickerhistory = dict()

    def set_tickerhistory(self, period: str, interval: str):
        """Downloads tickerhistory for period and interval in arg"""
        self.tickerhistory[interval] = self.ticker.history(period = period, interval = interval, prepost=True)

    def get_tickerhistory(self, period: str):
        """returns tickerhistory from tickerwrapper in memory for predefined period"""
        interval = setTickerArgs(period)
        return self.tickerhistory[interval]
        
    def verify_tickerhistory_exists(self, period: str) -> bool:
        """Checks if tickerhistory for this period already exists in model.tickerlist"""
        interval = setTickerArgs(period)
        if interval in self.tickerhistory:
            return True
        else:
            return False
        
    def verify_tickerhistory_valid(self, period: str):
        """This function verifies all data access, which will be made in Mainview to get data for table_watchlist"""
        try:
            interval = setTickerArgs(period)
            lastDataframeIndex = self.tickerhistory['1m'].shape[0]-1
            openprice = self.tickerhistory['1m']['Open'].values[lastDataframeIndex].item()
            delta_start = self.tickerhistory[interval]['Open'].values[0].item()
            return True
        except:
            print("This tickerhistory does not contain all required data, which is needed to table_watchlist")
            return False

    def verify_period_valid(self, period: str) -> bool:
        """This function verifies if the period in arg for this ticker is valid.
            Can only be called if tickerhistory for any period or interval was downloaded once for this ticker"""
        if period in self.ticker._price_history._history_metadata['validRanges']:
            return True
        else:
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
