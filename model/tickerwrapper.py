import yfinance as yf
from utils.helpfunctions import *
import pandas as pd

class TickerWrapper:

    def __init__(self) -> None:
        self.ticker = None
        self.tickerhistory = dict()
        self.tickerhistory_currency = dict()

    def set_ticker_yfinance(self, symbol: str) -> None:
        self.ticker = yf.Ticker(symbol)

    def set_tickerhistory_yfinance(self, period: str, interval: str) -> None:
        """Downloads tickerhistory for period and interval in arg"""
        self.tickerhistory[interval] = self.ticker.history(period = period, interval = interval, prepost=True)
        self.tickerhistory_currency[interval] = self.get_currency()

    def get_tickerhistory_memory(self, period: str):
        """returns tickerhistory from tickerwrapper in memory for predefined period"""
        interval = setTickerArgs(period)
        return self.tickerhistory[interval]
        
    def verify_tickerhistory_exists(self, period: str) -> bool:
        """Checks if tickerhistory for this period already exists in model.tickerwrappers"""
        interval = setTickerArgs(period)
        if interval in self.tickerhistory:
            return True
        else:
            return False
        
    def verify_tickerhistory_valid(self, period: str) -> bool:
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

    def update_tickerhistory(self,period: str, verify_period: bool) -> None:
        """Updates tickerhistory for predefined period with verifying if 
        period range is valid and optionally by optimizing interval"""
        interval = setTickerArgs(period)
        if self.verify_tickerhistory_exists(period = period):
            return
        if not verify_period:
            self.set_tickerhistory_yfinance(period, interval)
            return
        if not self.verify_period_valid(period = period):
            period = 'max'
            interval = setTickerArgs(period)
        self.set_tickerhistory_yfinance(period, interval) # period=max and use interval argument to avoid interval adaptation based on period

    def verify_currency_conversion_required(self):
        """Verifies if currency conversion is required"""
        currency = self.get_currency()
        if not currency == "EUR":
            return True
        else:
            return False
        
    def get_currency(self):
        currency = self.ticker.fast_info['currency']
        return currency
    
    def verify_tickerhistory_converted_already(self, currency_destination: str, interval: str):
        if self.tickerhistory_currency[interval] == currency_destination:
            return True
        else:
            return False

    def verify_currencywrapper_exists_in_memory(self, currencywrappers: dict):
        currency = self.get_currency()
        if currency in currencywrappers:
            return True
        else:
            return False