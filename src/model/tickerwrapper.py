import yfinance as yf
from model.historymanager import *
import pandas as pd
import time
from datetime import datetime

import requests_cache

class TickerWrapper:

    def __init__(self) -> None:
        self.ticker = None
        self.tickerhistory = dict()
        self.tickerhistory_currency = dict()

    def set_ticker_yfinance(self, symbol: str, session: requests_cache.CachedSession) -> None:
        self.ticker = yf.Ticker(symbol, session=session)

    def set_tickerhistory_yfinance(self, period: Period_Tickerhistory, interval: str) -> None:
        """Downloads tickerhistory for period and interval in arg"""
        self.tickerhistory[interval] = self.ticker.history(period = period, interval = interval, prepost=True, auto_adjust=False) # turned off repair, because for period=2y the download takes way too long
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
            #lastDataframeIndex = self.tickerhistory['1m'].shape[0]-1
            openprice = self.tickerhistory['1m']['Open'].values[-1].item()
            delta_start = self.tickerhistory[interval]['Open'].values[0].item()
            timestamp_today = self.tickerhistory['1m'].index
            return True
        except:
            print(f'{self.ticker.info["symbol"]} does not contain all required data, which is needed to table_watchlist')
            return False
        
    #def verify_current_tickerhistory_valid(self) -> bool:
    #    try:
    #        temp_current = self.tickerhistory["current"]["Close"][0]
    #        return True
    #    except:
    #        print("Current history does not contain any data. Will be set invalid for this period")
    #        return False

    def verify_period_valid(self, period: Period_Tickerhistory) -> bool:
        """This function verifies if the period in arg for this ticker is valid.
            Can only be called if tickerhistory for any period or interval was downloaded once for this ticker"""
        if period in self.ticker._price_history._history_metadata['validRanges']:
            return True
        else:
            return False
        
    def verify_financials_valid(self) -> bool:
        """Verifies that the downloaded ticker is a valid one (to prevent empty tickers)"""
        # trailingPegRatio is the best identifier which I found so far, improvable!
        try:
            trailing_pe = self.ticker.info['trailingPE']
            forward_pe = self.ticker.info['forwardPE']
            income = self.ticker.financials.loc["Net Income"]
            revenue = self.ticker.financials.loc["Total Revenue"]
        except:
            return False

    def verify_ticker_valid(self) -> bool:
        dict_invalid_ticker = {'trailingPegRatio': None}
        #workaround with try except, in case it takes very long to get the data 
        try:
            if self.ticker.info != dict_invalid_ticker:
                return True
            else:
                print("Tickerinformation invalid. Recheck entered ticker symbol!")
                return False   
        except:
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

        #new approach
        timezone = self.tickerhistory[interval].index.tz
        today_midnight = pd.Timestamp.now(tz=timezone).normalize()

        if period == '1d':
            midnight = today_midnight
            for days in range(1,5): # TODO: hardcoded fpr period="5d", retrieve 5 instead from period enum!
                if not self.tickerhistory[interval].index[-1] >= midnight:
                    midnight = midnight - pd.Timedelta(days=days)
                    continue
                timestamp_today = self.tickerhistory[interval].index[self.tickerhistory[interval].index >= midnight][0]
                self.tickerhistory["current"] = self.tickerhistory[interval].loc[timestamp_today:]
                break
        elif period == '3mo':
            three_months_ago = today_midnight - pd.tseries.offsets.DateOffset(months=3)
            timestamp_three_months_ago = self.tickerhistory[interval].index[self.tickerhistory[interval].index >= three_months_ago][0]
            self.tickerhistory["current"] = self.tickerhistory[interval].loc[timestamp_three_months_ago:]
        elif period == '6mo':
            six_months_ago = today_midnight - pd.tseries.offsets.DateOffset(months=6)
            timestamp_six_months_ago = self.tickerhistory[interval].index[self.tickerhistory[interval].index >= six_months_ago][0]
            self.tickerhistory["current"] = self.tickerhistory[interval].loc[timestamp_six_months_ago:]
        elif period == '1y':
            one_year_ago = today_midnight - pd.tseries.offsets.DateOffset(years=1)
            timestamp_one_year_ago = self.tickerhistory[interval].index[self.tickerhistory[interval].index >= one_year_ago][0]
            self.tickerhistory["current"] = self.tickerhistory[interval].loc[timestamp_one_year_ago:]
        elif period == '5y':
            five_years_ago = today_midnight - pd.tseries.offsets.DateOffset(years=5)
            timestamp_five_years_ago = self.tickerhistory[interval].index[self.tickerhistory[interval].index >= five_years_ago][0]
            self.tickerhistory["current"] = self.tickerhistory[interval].loc[timestamp_five_years_ago:]
        elif period == '10y':
            ten_years_ago = today_midnight - pd.tseries.offsets.DateOffset(years=10)
            timestamp_ten_years_ago = self.tickerhistory[interval].index[self.tickerhistory[interval].index >= ten_years_ago][0]
            self.tickerhistory["current"] = self.tickerhistory[interval].loc[timestamp_ten_years_ago:]
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