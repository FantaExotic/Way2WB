import yfinance as yf
from model.historymanager import *
import pandas as pd
import time
from datetime import datetime

class TickerWrapper:

    def __init__(self) -> None:
        self.ticker = None
        self.tickerhistory = dict()
        self.tickerhistory_currency = dict()

    def set_ticker_yfinance(self, symbol: str) -> None:
        self.ticker = yf.Ticker(symbol)

    def set_tickerhistory_yfinance(self, period: Period_Tickerhistory, interval: str) -> None:
        """Downloads tickerhistory for period and interval in arg"""
        self.tickerhistory[interval] = self.ticker.history(period = period, interval = interval, prepost=True, auto_adjust=False)
        self.tickerhistory_currency[interval] = self.get_currency()

    def get_tickerhistory_memory(self, period: Period_Tickerhistory):
        """returns tickerhistory from tickerwrapper in memory for predefined period"""
        interval = assign_period_to_interval(period)
        return self.tickerhistory[interval]
        
    def verify_tickerhistory_exists(self, period: Period_Tickerhistory) -> bool:
        """Checks if tickerhistory for this period already exists in model.tickerwrappers"""
        interval = assign_period_to_interval(period)
        if interval in self.tickerhistory:
            return True
        else:
            return False
        
    def verify_tickerhistory_valid(self, period: Period_Tickerhistory) -> bool:
        """This function verifies all data access, which will be made in Mainview to get data for table_watchlist"""
        try:
            interval = assign_period_to_interval(period)
            lastDataframeIndex = self.tickerhistory['1m'].shape[0]-1
            openprice = self.tickerhistory['1m']['Open'].values[lastDataframeIndex].item()
            delta_start = self.tickerhistory[interval]['Open'].values[0].item()
            return True
        except:
            print("This tickerhistory does not contain all required data, which is needed to table_watchlist")
            return False

    def verify_period_valid(self, period: Period_Tickerhistory) -> bool:
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

    def overwrite_tickerhistory(self, period: Period_Tickerhistory, verify_period: bool) -> None:
        """Overwrites tickerhistory. This is needed if period='5d' shall be analyzed after startup (default period='5d')"""
        interval = assign_period_to_interval(period)
        if not verify_period:
            self.set_tickerhistory_yfinance(period, interval)
            return
        if not self.verify_period_valid(period = period):
            period = 'max'
            interval = assign_period_to_interval(period)
        self.set_tickerhistory_yfinance(period, interval) # period=max and use interval argument to avoid interval adaptation based on period

    def update_tickerhistory(self, period: Period_Tickerhistory, verify_period: bool) -> None:
        """Updates tickerhistory for predefined period with verifying if 
        period range is valid and optionally by optimizing interval"""
        largest_period_for_same_interval = get_largest_period_for_same_interval(period)
        if self.verify_tickerhistory_exists(period = largest_period_for_same_interval):
            return
        self.overwrite_tickerhistory(period=largest_period_for_same_interval, verify_period=verify_period)

    def update_current_tickerhistory(self, period: Period_Tickerhistory):
        largest_period_for_same_interval = get_largest_period_for_same_interval(period)
        interval = assign_period_to_interval(largest_period_for_same_interval)
        
        timestamp_ticker_start = self.ticker.history_metadata['firstTradeDate'] # first ticker date
        timestamp_now = int(time.time())
        timestamp_delta = timestamp_now - timestamp_ticker_start
        tickerhistory_rows = self.tickerhistory[interval].shape[0]-1  # gets amount of rows in tickerhistory
        tickerhistory_years = (timestamp_delta / 60 / 60 / 24) // 365 # converts timestamp delta to total years

        len_tickerhistory_large_period = len(self.tickerhistory[interval])

        if period == '1d':
            len_tickerhistory_period = len_tickerhistory_large_period // 5 # because max period for "1d" is "5d"
            self.tickerhistory["current"] = self.tickerhistory[interval].iloc[(4*len_tickerhistory_period):]
        elif period == '3mo':
            len_tickerhistory_period = len_tickerhistory_large_period // 8
            self.tickerhistory["current"] = self.tickerhistory[interval].iloc[(7*len_tickerhistory_period):]
        elif period == '6mo':
            len_tickerhistory_period = len_tickerhistory_large_period // 4
            self.tickerhistory["current"] = self.tickerhistory[interval].iloc[(3*len_tickerhistory_period):]
        elif period == '1y':
            len_tickerhistory_period = len_tickerhistory_large_period // 2
            self.tickerhistory["current"] = self.tickerhistory[interval].iloc[len_tickerhistory_period:]
        elif period == '5y':
            index_5y = round(len_tickerhistory_large_period - (tickerhistory_rows / tickerhistory_years * 5))
            self.tickerhistory["current"] = self.tickerhistory[interval].iloc[index_5y:]
        elif period == '10y':
            index_10y = round(len_tickerhistory_large_period - (tickerhistory_rows / tickerhistory_years * 10))
            self.tickerhistory["current"] = self.tickerhistory[interval].iloc[index_10y:]
        else:
            self.tickerhistory["current"] = self.tickerhistory[interval]

        self.tickerhistory_currency["current"] = self.tickerhistory_currency[interval]

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