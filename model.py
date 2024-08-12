import yfinance as yf
import json
from pathlib import Path
import os

class Model:
    def __init__(self):
        self.tickerlist = list()
        self.basepath = Path(__file__).resolve().parent
        self.watchlistfile = self.basepath.joinpath("watchlist.json")  # configfile containing watchlist
        self.methods = []
        self.movingaverage_symbol = "MA"
        self.valid_period_1minute = {"1d": "1 day", 
                                     "5d": "5 days"}
        self.valid_period_5minutes = {"1mo": "1 month"}
        self.valid_period_1hour = {"3mo": "3 months",
                                    "6mo": "6 months",
                                    "1y": "1 year",
                                    "2y": "2 years",}
        self.valid_period_1day = {"5y": "5 years",
                                    "10y": "10 years",
                                    "ytd": "This year",
                                    "max": "Maximum period"}
        self.valid_periods = self.valid_period_1minute | self.valid_period_5minutes | self.valid_period_1hour | self.valid_period_1day
        self.initWatchlist()

    #checks if 
    def checkWatchlist(self):
        
        if not os.path.exists(self.watchlistfile):
            print("Watchlistfile not found!")
            Path(self.watchlistfile).touch()
            return False
        
        if not os.path.getsize(self.watchlistfile)>0:
            print("Watchlistfile is empty!")
            return False
        
        return True

    def getWatchlist(self,ticker):

        # Load existing data from the JSON file
        with open(self.watchlistfile, 'r') as file:
            data = json.load(file)

        # extract each[0] (symbol) from each element in data, to check for duplicates
        tmpdata = [each[0] for each in data]
        if ticker.info["symbol"] in tmpdata:
            print("Stock already exists in Watchlist!")
            return 0

    def initWatchlist(self):
        if not self.checkWatchlist():
            return

        # Load existing data from the JSON file
        with open(self.watchlistfile, 'r') as file:
            data = json.load(file)

        for each in data:
            ticker = self.findTicker(each[0])  # each[0] = symbol, each[1] = shortName
            if ticker:
                self.add_stock_to_tickerlist(ticker)

    def findTicker(self,symbol) -> yf.Ticker:
        if not symbol:
            print("Symbol empty! Ticker couldnt be generated for this symbol!")
            return None
        ticker = yf.Ticker(symbol)
        try:
            check = ticker.info['symbol']
            check = ticker.info['shortName']
            check = ticker.isin
        except:
            print("Tickerinfo about symbol, shortname and isin doesnt exist. Recheck entered symbol!")
            return None
        #self.symbol_info_label.config(text=f"Stock Symbol found: True\nShortname: {short_name}\nSymbol: {symbol}\nISIN: {isin}")
        return ticker
    
    def add_stock_to_tickerlist(self,ticker):
        self.tickerlist.append(ticker)

    def remove_stock_from_tickerlist(self,ticker_symbol):
        for ticker in self.tickerlist:
            if ticker.info["symbol"] == ticker_symbol:
                self.tickerlist.remove(ticker)

    def add_stockticker_to_watchlistfile(self,ticker):
        
        if not self.checkWatchlist():
            return

        # Load existing data from the JSON file
        with open(self.watchlistfile, 'r') as file:
            data = json.load(file)

        # Save the updated data back to the JSON file
        data.append([ticker.info["symbol"], ticker.info["shortName"]])
        with open(self.watchlistfile, 'w') as file:
            json.dump(data, file, indent=4)
    
    def check_duplicates_in_watchlistfile(self,ticker):
        # Load existing data from the JSON file
        with open(self.watchlistfile, 'r') as file:
            data = json.load(file)
    
        # extract each[0] (symbol) from each element in data, to check for duplicates
        tmpdata = [each[0] for each in data]
        if ticker.info["symbol"] in tmpdata:
            print("Stock already exists in Watchlist!")
            return True
        else:
            return False

    def remove_stockticker_from_watchlistfile(self,symbol):

        check = self.checkWatchlist()
        if not check:
            return

        with open(self.watchlistfile, 'r') as file:
            data = json.load(file)

        # extract each[0] (symbol) from each element in data, to check for duplicates
        tmpdata = [each[0] for each in data]
        for index,each in enumerate(tmpdata):
            if each == symbol:
                data.pop(index)

        with open(self.watchlistfile, 'w') as file:
            json.dump(data, file, indent=4)


    def remove_method(self,index):
        #TODO: rework!
        pass

################################################################################
## 
## Helpfunction:
## setTickerArgs
##  
## Description:
## This function adjusts the argument interval for yf.Ticker call based 
## on the period argument, otherwise YFInvalidPeriodError will be thrown in
## scrapers/history.py
## Period/Interval relationship is hardcoded based on codesnipped from line 98-106
## 
################################################################################
    def setTickerArgs(self, period: str) -> str:
        if period in self.valid_period_1minute.keys():
            interval = "1m"
        elif period in self.valid_period_5minutes.keys():
            interval = "5m"
        elif period in self.valid_period_1hour.keys():
            interval = "1h"
        elif period in self.valid_period_1day.keys():
            interval = "1d"
        else:
            print("period not matching any element in self.valid_periods. default: interval = 1d")
            interval = "1d"
        return interval