import json
from model.tickerwrapper import TickerWrapper
import pandas as pd
from model.watchlistfile import Watchlistfile
from model.currency import CurrencyWrapper
from model.liveticker.liveticker import Liveticker
from model.historymanager import *
from model.rule import Rule

import requests_cache
import asyncio

class Model:
    def __init__(self):
        self.tickerwrappers = dict()
        self.currencywrappers = dict()
        self.watchlistfile = Watchlistfile()
        self.methods = dict()
        self.liveticker = Liveticker()
        #self.notifier = Notifier()
        self.rules = []

    #def init_model(self):
    #    self.session = self.init_session()
    #    self.init_tickerwrappers()

    def init_session(self) -> requests_cache.CachedSession:
        #TODO: remove init_session(), since it became obsolete
        session = requests_cache.CachedSession('yfinance.cache')
        session.headers['User-Agent'] = "my-program/1.0"
        return session

    #def init_tickerwrappers(self) -> None:
    #    """initializes tickerwrappers based on data from tickerwrapperfile. Ticker and tickerhistory for period '5d'
    #        will be downloaded and checked for the existence of data, which is required in table watchlist"""
    #    if not self.watchlistfile.check_watchlistfile():
    #        return
    #    with open(self.watchlistfile.watchlistfilePath, 'r') as file:
    #        data = json.load(file)
    #    for each in data:
    #        tickerwrapper = self.get_tickerwrapper_yfinance(each[0])  # each[0] = symbol, each[1] = shortName
    #        if not tickerwrapper.verify_ticker_valid():
    #            continue
    #        tickerwrapper.update_tickerhistory(period='5d', verify_period=False)
    #        if not tickerwrapper.verify_tickerhistory_valid(period="5d"):
    #            continue
    #        tickerwrapper.update_current_tickerhistory(period="5d")
    #        tickerwrapper = self.wrapper_convert_currency(tickerwrapper=tickerwrapper)
    #        self.add_tickerwrapper_to_tickerwrappers(tickerwrapper=tickerwrapper)

    #def get_tickerwrapper_yfinance(self, symbol: str) -> TickerWrapper:
    #    """Downloads and returns ticker for symbol in arg"""
    #    tickerwrapper = TickerWrapper()
    #    tickerwrapper.set_ticker_yfinance(symbol=symbol, session=self.session)
    #    return tickerwrapper

    async def get_tickerwrapper_yfinance_async(self, symbol: str) -> TickerWrapper:
        """Async version of get_tickerwrapper_yfinance"""
        #loop = asyncio.get_event_loop()
        #tickerwrapper = TickerWrapper()
        #await loop.run_in_executor(None, tickerwrapper.set_ticker_yfinance, symbol, self.session)
        #return tickerwrapper
        tickerwrapper = TickerWrapper()
        await tickerwrapper.set_ticker_yfinance_async(symbol=symbol, session=self.session)
        return tickerwrapper

    def get_currencywrapper_yfinance(self, tickerwrapper: TickerWrapper) -> CurrencyWrapper:
        currencywrapper = CurrencyWrapper()
        currencywrapper.currencysource = tickerwrapper.ticker.info_local['currency']
        currencywrapper.currencysymbol = f'{currencywrapper.currencysource}{currencywrapper.currencydestination}=x'
        currencywrapper.set_ticker_yfinance(symbol=currencywrapper.currencysymbol, session=self.session)
        return currencywrapper

    def update_tickerhistories(self,period: Period_Tickerhistory, verify_period: bool) -> None:
        """Updates tickerhistory for all tickers in tickerlist"""
        for tickerwrapper in self.tickerwrappers.values():
            tickerwrapper: TickerWrapper
            tickerwrapper.update_tickerhistory(period=period, verify_period=verify_period)
            tickerwrapper.update_current_tickerhistory(period=period)

    def add_tickerwrapper_to_tickerwrappers(self,tickerwrapper: TickerWrapper) -> None:
        """adds tickerwrapper to tickerwrappers"""
        self.tickerwrappers[tickerwrapper.ticker.info_local["symbol"]] = tickerwrapper

    def overwrite_tickerwrapper_in_tickerwrappers(self, tickerwrapper: TickerWrapper) -> None:
        """overwrite existing tickerwrapper in tickerwrappers. This is needed if bigger period for same interval will be downloadedp"""
        tickerwrapper.overwrite_tickerhistory()
        self.tickerwrappers[tickerwrapper.ticker.info_local["symbol"]] = tickerwrapper

    def remove_tickerwrapper_from_tickerwrappers(self,ticker_symbol: str) -> None:
        """removes tickerwrapper with symbol in arg from tickerwrappers"""
        for key, tickerwrapper in self.tickerwrappers.items():
            if tickerwrapper.ticker.info_local["symbol"] == ticker_symbol:
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
        if self.verify_currencywrapper_exists_in_memory(currency=currency):
            currencywrapper = self.currencywrappers[currency]
        else:
            currencywrapper = self.get_currencywrapper_yfinance(tickerwrapper=tickerwrapper)
        tickerwrapper = currencywrapper.convert_currency_in_tickerhistory(tickerwrapper=tickerwrapper)
        if not self.verify_currencywrapper_exists_in_memory(currency=currency):
            self.currencywrappers[currency] = currencywrapper
        return tickerwrapper
    
    def add_rule(self, threshold: int, symbol: str, period: Period_Tickerhistory):
        """create rule based on input from 'notifier and rules' view and add data to model"""
        rule = Rule()
        rule.create_rule(threshold=threshold, symbol=symbol, shortname=self.tickerwrappers[symbol].ticker.info_local["symbol"], period=period, activated=True)
        self.rules.append(rule)
        self.rules

    def wrapper_convert_currencies(self):
        for tickerwrapper in self.tickerwrappers.values():
            tickerwrapper: TickerWrapper
            tickerwrapper = self.wrapper_convert_currency(tickerwrapper=tickerwrapper)

    def verify_currencywrapper_exists_in_memory(self, currency: str):
        if currency in self.currencywrappers:
            return True
        return False

    """Wrapperfunctions for functions in Watchlistfile"""

    def add_tickerinfo_to_watchlistfile(self, tickerwrapper: TickerWrapper) -> None:
        """Wrapperfunction for add_tickerinfo_to_watchlistfile in Watchlistfile"""
        self.watchlistfile.add_tickerinfo_to_watchlistfile(symbol=tickerwrapper.ticker.info_local["symbol"], shortName=tickerwrapper.ticker.info_local["shortName"])

    def check_duplicates_in_watchlistfile(self, tickerwrapper: TickerWrapper) -> bool:
        """Wrapperfunction for check_duplicates_in_watchlistfile in Watchlistfile"""
        return self.watchlistfile.check_duplicates_in_watchlistfile(symbol=tickerwrapper.ticker.info_local["symbol"])
    
    def update_liveticker(self, msg: dict):
        #tickersymbol = self.tickerwrappers[msg['id']]
        symbol = msg['id']
        tickerwrapper: TickerWrapper
        tickerwrapper = self.tickerwrappers[symbol]
        currencywrapper: CurrencyWrapper
        currencywrapper = self.currencywrappers[tickerwrapper.get_currency()]
        self.liveticker.append_liveticker_to_tickerwrapper(msg=msg, tickerwrapper=tickerwrapper, currencywrapper=currencywrapper)

    async def init_tickerwrappers_async(self) -> None:
        """Async version of init_tickerwrappers"""
        if not self.watchlistfile.check_watchlistfile():
            return
        with open(self.watchlistfile.watchlistfilePath, 'r') as file:
            data = json.load(file)
        
        for each in data:
            tickerwrapper = await self.get_tickerwrapper_yfinance_async(each[0])
            if not tickerwrapper.verify_ticker_valid():
                continue
            await tickerwrapper.update_tickerhistory_async(period='5d', verify_period=False)
            if not tickerwrapper.verify_tickerhistory_valid(period="5d"):
                continue
            tickerwrapper.update_current_tickerhistory(period="5d")
            tickerwrapper = self.wrapper_convert_currency(tickerwrapper=tickerwrapper)
            self.add_tickerwrapper_to_tickerwrappers(tickerwrapper=tickerwrapper)

    async def init_model_async(self):
        """Async version of init_model"""
        self.session = self.init_session()
        await self.init_tickerwrappers_async()