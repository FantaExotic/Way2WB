import json
from model.tickerwrapper import TickerWrapper
from utils.helpfunctions import *
import pandas as pd
from model.watchlistfile import Watchlistfile
from model.currency import CurrencyWrapper
from model.liveticker.liveticker import Liveticker

class Model:
    def __init__(self):
        self.tickerwrappers = dict()
        self.currencywrappers = dict()
        self.watchlistfile = Watchlistfile()
        self.methods = dict()
        self.liveticker = Liveticker()
        self.init_tickerwrappers()

    def init_tickerwrappers(self) -> None:
        """initializes tickerwrappers based on data from tickerwrapperfile. Ticker and tickerhistory for period '1d'
            will be downloaded and checked for the existence of data, which is required in table watchlist"""
        if not self.watchlistfile.check_watchlistfile():
            return
        with open(self.watchlistfile.watchlistfilePath, 'r') as file:
            data = json.load(file)
        for each in data:
            tickerwrapper = self.get_tickerwrapper_yfinance(each[0])  # each[0] = symbol, each[1] = shortName
            if not tickerwrapper.verify_ticker_valid():
                continue
            tickerwrapper.update_tickerhistory(period='1d', verify_period=False)
            if not tickerwrapper.verify_tickerhistory_valid(period="1d"):
                continue
            tickerwrapper = self.wrapper_convert_currency(tickerwrapper=tickerwrapper)
            self.add_tickerwrapper_to_tickerwrappers(tickerwrapper=tickerwrapper)

    def get_tickerwrapper_yfinance(self, symbol: str) -> TickerWrapper:
        """Downloads and returns ticker for symbol in arg"""
        tickerwrapper = TickerWrapper()
        tickerwrapper.set_ticker_yfinance(symbol)
        return tickerwrapper

    def get_currencywrapper_yfinance(self, tickerwrapper: TickerWrapper) -> CurrencyWrapper:
        currencywrapper = CurrencyWrapper()
        currencywrapper.currencysource = tickerwrapper.ticker.info['currency']
        currencywrapper.currencysymbol = f'{currencywrapper.currencysource}{currencywrapper.currencydestination}=x'
        currencywrapper.set_ticker_yfinance(currencywrapper.currencysymbol)
        return currencywrapper

    def update_tickerhistories(self,period: str, verify_period: bool) -> None:
        """Updates tickerhistory for all tickers in tickerlist"""
        for tickerwrapper in self.tickerwrappers.values():
            tickerwrapper: TickerWrapper
            tickerwrapper.update_tickerhistory(period=period, verify_period=verify_period)

    def add_tickerwrapper_to_tickerwrappers(self,tickerwrapper: TickerWrapper) -> None:
        """adds tickerwrapper to tickerwrappers"""
        self.tickerwrappers[tickerwrapper.ticker.info["symbol"]] = tickerwrapper

    def remove_tickerwrapper_from_tickerwrappers(self,ticker_symbol: str) -> None:
        """removes tickerwrapper with symbol in arg from tickerwrappers"""
        for key, tickerwrapper in self.tickerwrappers.items():
            if tickerwrapper.ticker.info["symbol"] == ticker_symbol:
                del self.tickerwrappers[key]
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

    def wrapper_convert_currency(self, tickerwrapper: TickerWrapper) -> TickerWrapper:
        """Wrapper for currency update, needed to use/update currencywrapper in currencywrappers"""
        currency = tickerwrapper.get_currency()
        if tickerwrapper.verify_currencywrapper_exists_in_memory(currencywrappers=self.currencywrappers):
            currencywrapper = self.currencywrappers[currency]
        else:
            currencywrapper = self.get_currencywrapper_yfinance(tickerwrapper=tickerwrapper)
        tickerwrapper = currencywrapper.convert_currency_in_tickerhistory(tickerwrapper=tickerwrapper)
        if not tickerwrapper.verify_currencywrapper_exists_in_memory(currencywrappers=self.currencywrappers):
            self.currencywrappers[currency] = currencywrapper
        return tickerwrapper

    def wrapper_convert_currencies(self):
        for tickerwrapper in self.tickerwrappers.values():
            tickerwrapper: TickerWrapper
            tickerwrapper = self.wrapper_convert_currency(tickerwrapper=tickerwrapper)

    """Wrapperfunctions for functions in Watchlistfile"""

    def add_tickerinfo_to_watchlistfile(self, tickerwrapper: TickerWrapper) -> None:
        """Wrapperfunction for add_tickerinfo_to_watchlistfile in Watchlistfile"""
        self.watchlistfile.add_tickerinfo_to_watchlistfile(symbol=tickerwrapper.ticker.info["symbol"], shortName=tickerwrapper.ticker.info["shortName"])

    def check_duplicates_in_watchlistfile(self, tickerwrapper: TickerWrapper) -> bool:
        """Wrapperfunction for check_duplicates_in_watchlistfile in Watchlistfile"""
        return self.watchlistfile.check_duplicates_in_watchlistfile(symbol=tickerwrapper.ticker.info["symbol"])
    
    def update_liveticker(self, msg: dict):
        tickersymbol = self.tickerwrappers[msg['id']]
        tickerwrapper: TickerWrapper
        tickerwrapper = self.tickerwrappers[tickersymbol]
        currencywrapper: CurrencyWrapper
        currencywrapper = self.currencywrappers[tickerwrapper.get_currency()]
        self.liveticker.append_liveticker_to_tickerwrapper(msg=msg, tickerwrapper=tickerwrapper, currencywrapper=currencywrapper)