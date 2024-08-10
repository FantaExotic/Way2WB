import yfinance as yf
import json
from pathlib import Path
import os

class Model:
    def __init__(self):
        self.tickerlist = list()
        self.date_start = None
        self.date_end = None
        self.watchlist_input = None # to add to watchlist
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

    def initWatchlist(self):
        #TODO: do error handling if yt.ticker wasnt found
        try:
            if os.path.exists(self.watchlistfile) and os.path.getsize(self.watchlistfile)>0:
                #TODO: check if file exists, otherwise create file
                # Load existing data from the JSON file
                with open(self.watchlistfile, 'r') as file:
                    data = json.load(file)
                for each in data:
                    self.tickerlist.append(yf.Ticker(each[0]))  # each[0] = symbol, each[1] = shortName
            else:
                pass
        except FileNotFoundError:
            print("Initializing Watchlist failed")
            # If the file does not exist, initialize an empty list

    def findTicker(self,symbol) -> yf.Ticker:
        # Update the start and end dates
        if symbol:
            ticker = yf.Ticker(symbol)
            # check to verify if valid ticker was found by checking some info
            check = ticker.info['symbol']
            #self.symbol_info_label.config(text=f"Stock Symbol found: True\nShortname: {short_name}\nSymbol: {symbol}\nISIN: {isin}")
            self.tickerlist.append(symbol)
            return ticker


    def add_stockticker_to_watchlist(self,ticker):
        try:
            data = []
            if os.path.exists(self.watchlistfile) and os.path.getsize(self.watchlistfile)>0:
                #TODO: check if file exists, otherwise create file
                # Load existing data from the JSON file
                with open(self.watchlistfile, 'r') as file:
                    data = json.load(file)
            else:
                Path(self.watchlistfile).touch()

            # extract each[0] (symbol) from each element in data, to check for duplicates
            tmpdata = [each[0] for each in data]

            # Add the new stock ticker entry
            if not ticker.info["symbol"] in tmpdata:
                data.append([ticker.info["symbol"], ticker.info["shortName"]])
                #TODO: add stockticker to self.watchlist variable
                # Save the updated data back to the JSON file
                with open(self.watchlistfile, 'w') as file:
                    json.dump(data, file, indent=4)
                return 1    # return value controls if stockticker is duplicate in data
            else:
                return 0
            
        except FileNotFoundError:
            print("watchlistfile not found. Couldnt add stock from watchlist!")

    def remove_stockticker_from_watchlist(self,symbol):
        try:
            if os.path.exists(self.watchlistfile) and os.path.getsize(self.watchlistfile)>0:
                data = []
                with open(self.watchlistfile, 'r') as file:
                    data = json.load(file)

                # extract each[0] (symbol) from each element in data, to check for duplicates
                tmpdata = [each[0] for each in data]
                
                for index,each in enumerate(tmpdata):
                    if each == symbol:
                        data.pop(index)
                        #TODO: recheck removing from list while iterating through it, because of mutable/immutable objects!!!!!
                with open(self.watchlistfile, 'w') as file:
                    json.dump(data, file, indent=4)

        except FileNotFoundError:
            print("watchlistfile not found. Couldnt remove stock from watchlist!")

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