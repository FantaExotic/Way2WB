import yfinance as yf
import json
from pathlib import Path
import os
from model.tickerwrapper import TickerWrapper
import yliveticker as ylt
from utils.helpfunctions import *
import numpy as np
import pandas as pd
from datetime import datetime, timezone

class Model:
    def __init__(self):
        self.tickerlist = list()
        self.basepath = Path(__file__).resolve().parent
        self.watchlistfile = self.basepath.joinpath("watchlist.json")  # configfile containing watchlist
        self.methods = []
        self.movingaverage_symbol = "MA"
        #self.yliveticker = None
        self.initWatchlist()
        self.update_tickerhistory(period='1d', verify_period=False)

    def handle_liveticker_update(self, msg):
        # Update ticker data here based on the received message
        for index,tickerwrapper in enumerate(self.tickerlist):
            if tickerwrapper.ticker.info['symbol'] == msg['id']:
                #price = msg['price']
                price = msg['price']
                timestamp_ms = msg['timestamp']
                timestamp_s = timestamp_ms / 1000  # Convert milliseconds to seconds
                dayVolume = msg['dayVolume']
                new_value = {'Open': [price], 'High': [price], 'Low': [price], 'Close': [price], 'Volume': [dayVolume], 'Dividends': [222]}  # Replace with your new data

                # Convert new_value to a DataFrame with the appropriate index
                new_data = pd.DataFrame(new_value)
                new_data.index = pd.to_datetime([timestamp_s], unit="s")

                if new_data.index.tz is None:
                    new_data.index = new_data.index.tz_localize("UTC")
                new_data.index = new_data.index.tz_convert(tickerwrapper.ticker._tz)
                new_data.index.name = tickerwrapper.tickerhistory['1m'].index.name

                # Update the existing tickerhistory['1m'] DataFrame with the new data
                new_dataframe = pd.concat([self.tickerlist[index].tickerhistory['1m'],new_data])
                self.tickerlist[index].tickerhistory['1m'] = new_dataframe
                #TODO fix updating properties values and index (they are no attributes!)

    def initWatchlist(self) -> None:
        if not self.checkWatchlist():
            return

        # Load existing data from the JSON file
        with open(self.watchlistfile, 'r') as file:
            data = json.load(file)

        for each in data:
            tickerwrapper = self.findTicker(each[0])  # each[0] = symbol, each[1] = shortName
            if tickerwrapper.ticker:
                self.add_stock_to_tickerlist(tickerwrapper)

    #checks if 
    def checkWatchlist(self) -> bool:
        
        if not os.path.exists(self.watchlistfile):
            print("Watchlistfile not found!")
            Path(self.watchlistfile).touch()
            return False
        
        if not os.path.getsize(self.watchlistfile)>0:
            print("Watchlistfile is empty!")
            return False
        
        return True

    def getWatchlist(self,tickerwrapper: TickerWrapper) -> bool:

        # Load existing data from the JSON file
        with open(self.watchlistfile, 'r') as file:
            data = json.load(file)

        # extract each[0] (symbol) from each element in data, to check for duplicates
        tmpdata = [each[0] for each in data]
        if tickerwrapper.ticker.info["symbol"] in tmpdata:
            print("Stock already exists in Watchlist!")
            return False

    def findTicker(self,symbol: str) -> TickerWrapper:
        tickerwrapper = TickerWrapper(yf.Ticker(symbol))
        return tickerwrapper

    def update_tickerhistory(self,period: str, verify_period: bool):
        """Updates tickerhistory for predefined period with verifying if 
        period range is valid and optionally by optimizing interval"""
        interval = setTickerArgs(period)
        for tickerwrapper in self.tickerlist:
            if tickerwrapper.verify_tickerhistory_exists(period = period):
                continue
            if not verify_period:
                tickerwrapper.set_tickerhistory(period, interval)
                continue
            if not tickerwrapper.verify_period_valid(period = period):
                period = 'max'
                interval = setTickerArgs(period)
            tickerwrapper.set_tickerhistory(period, interval) # period=max and use interval argument to avoid interval adaptation based on period

    def add_stock_to_tickerlist(self,tickerwrapper: TickerWrapper) -> None:
        self.tickerlist.append(tickerwrapper)

    def remove_stock_from_tickerlist(self,ticker_symbol: str) -> None:
        for tickerwrapper in self.tickerlist:
            if tickerwrapper.ticker.info["symbol"] == ticker_symbol:
                self.tickerlist.remove(tickerwrapper)

    def add_stockticker_to_watchlistfile(self,tickerwrapper: TickerWrapper) -> None:
        
        if not self.checkWatchlist():
            return

        # Load existing data from the JSON file
        with open(self.watchlistfile, 'r') as file:
            data = json.load(file)

        # Save the updated data back to the JSON file
        data.append([tickerwrapper.ticker.info["symbol"], tickerwrapper.ticker.info["shortName"]])
        with open(self.watchlistfile, 'w') as file:
            json.dump(data, file, indent=4)

    def check_duplicates_in_watchlistfile(self,tickerwrapper: TickerWrapper) -> bool:
        # Load existing data from the JSON file
        with open(self.watchlistfile, 'r') as file:
            data = json.load(file)
    
        # extract each[0] (symbol) from each element in data, to check for duplicates
        tmpdata = [each[0] for each in data]
        if tickerwrapper.ticker.info["symbol"] in tmpdata:
            print("Stock already exists in Watchlist!")
            return True
        else:
            return False

    def remove_stockticker_from_watchlistfile(self,symbol: str) -> None:
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
