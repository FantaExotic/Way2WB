import yfinance as yf
import json
from pathlib import Path
import os

class Model:
    def __init__(self):
        self.stockdata = dict()
        self.shortname = dict() # lookup dict to identify shortname of symbol
        self.date_start = None
        self.date_end = None
        self.watchlist_input = None # to add to watchlist
        self.basepath = Path(__file__).resolve().parent
        self.watchlistfile = self.basepath.joinpath("watchlist.json")  # configfile containing watchlist

    def initWatchlist(self):
        try:
            if os.path.exists(self.watchlistfile) and os.path.getsize(self.watchlistfile)>0:
                #TODO: check if file exists, otherwise create file
                # Load existing data from the JSON file
                with open(self.watchlistfile, 'r') as file:
                    data = json.load(file)
                for each in data:
                    symbol,shortname = each # because shortname and symbol are splitted
                    temp= yf.download(symbol, period="max")
                    self.stockdata[symbol] = temp
                    self.shortname[symbol] = shortname # lookup dict to identify shortname of symbol
            else:
                pass
        except FileNotFoundError:
            pass
            # If the file does not exist, initialize an empty list

    def findTicker(self,symbol):
        # Update the start and end dates
        if symbol:
            try:
                self.data = yf.download(symbol, period="max")
                self.ticker = yf.Ticker(symbol)
                short_name = self.ticker.info['shortName']
                symbol = self.ticker.info['symbol']
                #isin = self.ticker.isin
                #self.symbol_info_label.config(text=f"Stock Symbol found: True\nShortname: {short_name}\nSymbol: {symbol}\nISIN: {isin}")
                return [symbol,short_name]
            except Exception as e:
                #self.symbol_info_label.config(text="Stock Symbol found: False\nShortname:\nSymbol:\nISIN:")
                return ""

    def add_stockticker_to_watchlist(self,stockticker):
        symbol,shortname = stockticker
        try:
            data = []
            if os.path.exists(self.watchlistfile) and os.path.getsize(self.watchlistfile)>0:
                #TODO: check if file exists, otherwise create file
                # Load existing data from the JSON file
                with open(self.watchlistfile, 'r') as file:
                    data = json.load(file)
            else:
                Path(self.watchlistfile).touch()
        except FileNotFoundError:
                    # If the file does not exist, initialize an empty list
                    data = []

        # Add the new stock ticker entry
        if not stockticker in data:
            data.append(stockticker)
            #TODO: add stockticker to self.watchlist variable
            # Save the updated data back to the JSON file
            with open(self.watchlistfile, 'w') as file:
                json.dump(data, file, indent=4)
            self.stockdata[symbol] = self.data
            self.shortname[symbol] = shortname
            return 1    # return value controls if stockticker is duplicate in data
        else:
            return 0