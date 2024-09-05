import yfinance as yf
import json
from model.tickerwrapper import TickerWrapper
from utils.helpfunctions import *
import pandas as pd
from model.watchlistfile import Watchlistfile

class Model:
    def __init__(self):
        self.tickerlist = dict()
        self.watchlistfile = Watchlistfile()
        self.methods = dict()
        self.init_tickerwrapperlist()

    def update_liveticker(self, msg: dict) -> None:
        """processes received data from liveticker and appends it to tickerhistory of corresponding ticker"""
        tickerwrapper = self.tickerlist[msg['id']]
        price = msg['price']
        timestamp_ms = msg['timestamp']
        timestamp_s = timestamp_ms / 1000  # Convert milliseconds to seconds
        dayVolume = msg['dayVolume']
        new_value = {'Open': [price], 'High': [price], 'Low': [price], 'Close': [price], 'Volume': [dayVolume], 'Dividends': [222]}  # Replace with your new data
        new_data = pd.DataFrame(new_value)
        new_data.index = pd.to_datetime([timestamp_s], unit="s")
        if new_data.index.tz is None:
            new_data.index = new_data.index.tz_localize("UTC")
        new_data.index = new_data.index.tz_convert(tickerwrapper.ticker._tz)
        new_data.index.name = tickerwrapper.tickerhistory['1m'].index.name
        # Update the existing tickerhistory['1m'] DataFrame with the new data
        new_dataframe = pd.concat([self.tickerlist[msg['id']].tickerhistory['1m'],new_data])
        self.tickerlist[msg['id']].tickerhistory['1m'] = new_dataframe

    def init_tickerwrapperlist(self) -> None:
        """initializes tickerwrapperlist based on data from tickerwrapperfile. Ticker and tickerhistory for period '1d'
            will be downloaded and checked for the existence of data, which is required in table watchlist"""
        if not self.watchlistfile.check_watchlistfile():
            return
        with open(self.watchlistfile.watchlistfilePath, 'r') as file:
            data = json.load(file)
        for each in data:
            tickerwrapper = self.get_tickerwrapper(each[0])  # each[0] = symbol, each[1] = shortName
            if not tickerwrapper.verify_ticker_valid():
                print("Ticker from watchlistfile invalid. Ticker will be ignored")
                continue
            self.update_tickerhistory(period='1d', verify_period=False, tickerwrapper=tickerwrapper)
            if not tickerwrapper.verify_tickerhistory_valid(period="1d"):
                print("Tickerhistory from ticker in watchlistfile invalid. Ticker will be ignored")
                continue
            self.add_tickerwrapper_to_tickerwrapperlist(tickerwrapper)

    def get_tickerwrapper(self,symbol: str) -> TickerWrapper:
        """Downloads and returns ticker for symbol in arg"""
        tickerwrapper = TickerWrapper(yf.Ticker(symbol))
        return tickerwrapper

    def update_tickerhistories(self,period: str, verify_period: bool) -> None:
        """Updates tickerhistory for all tickers in tickerlist"""
        for tickerwrapper in self.tickerlist.values():
            self.update_tickerhistory(period=period, verify_period=verify_period, tickerwrapper=tickerwrapper)

    def update_tickerhistory(self,period: str, verify_period: bool, tickerwrapper: TickerWrapper) -> None:
        """Updates tickerhistory for predefined period with verifying if 
        period range is valid and optionally by optimizing interval"""
        interval = setTickerArgs(period)
        if tickerwrapper.verify_tickerhistory_exists(period = period):
            return
        if not verify_period:
            tickerwrapper.set_tickerhistory(period, interval)
            return
        if not tickerwrapper.verify_period_valid(period = period):
            period = 'max'
            interval = setTickerArgs(period)
            print("max period used!")
        tickerwrapper.set_tickerhistory(period, interval) # period=max and use interval argument to avoid interval adaptation based on period

    def add_tickerwrapper_to_tickerwrapperlist(self,tickerwrapper: TickerWrapper) -> None:
        """adds tickerwrapper to tickerwrapperlist"""
        self.tickerlist[tickerwrapper.ticker.info["symbol"]] = tickerwrapper

    def remove_tickerwrapper_from_tickerwrapperlist(self,ticker_symbol: str) -> None:
        """removes tickerwrapper with symbol in arg from tickerwrapperlist"""
        for key, tickerwrapper in self.tickerlist.items():
            if tickerwrapper.ticker.info["symbol"] == ticker_symbol:
                del self.tickerlist[key]
                return

    def add_method(self, methodArg: int, method: str):
        """adds method to methods dict"""
        if not str(method) in self.methods:
            self.methods[method] = [methodArg]
        else:
            self.methods[method].append(methodArg)

    def remove_method(self, methodArg: str, method: str):
        """Removes method from methods dict"""
        self.methods[method].remove(methodArg)    

    """Wrapperfunctions for functions in Watchlistfile"""

    def add_tickerinfo_to_watchlistfile(self,tickerwrapper: TickerWrapper) -> None:
        """Wrapperfunction for add_tickerinfo_to_watchlistfile in Watchlistfile"""
        self.watchlistfile.add_tickerinfo_to_watchlistfile(symbol=tickerwrapper.ticker.info["symbol"], shortName=tickerwrapper.ticker.info["shortName"])

    def check_duplicates_in_watchlistfile(self,tickerwrapper: TickerWrapper) -> bool:
        """Wrapperfunction for check_duplicates_in_watchlistfile in Watchlistfile"""
        return self.watchlistfile.check_duplicates_in_watchlistfile(symbol=tickerwrapper.ticker.info["symbol"])