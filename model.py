import yfinance as yf
import json
from pathlib import Path

class Model:
    def __init__(self):
        self.selection = []     # selected stocks from list
        self.date_start = None
        self.date_end = None
        self.watchlist_input = None # to add to watchlist
        self.watchlist = "watchlist.json"  # configfile containing watchlist
    
    def findTicker(self,symbol):
        # Update the start and end dates
        if symbol:
            try:
                self.data = yf.download(symbol, period="max")
                self.ticker = yf.Ticker(symbol)
                short_name = self.ticker.info['shortName']
                symbol = self.ticker.info['symbol']
                isin = self.ticker.isin
                self.symbol_info_label.config(text=f"Stock Symbol found: True\nShortname: {short_name}\nSymbol: {symbol}\nISIN: {isin}")
                return [self.ticker.info['symbol'], self.ticker.info['shortName']]
            except Exception as e:
                self.symbol_info_label.config(text="Stock Symbol found: False\nShortname:\nSymbol:\nISIN:")
                return ""

    def add_stockticker_to_watchlist(self,stockticker):
        try:
            #TODO: check if file exists, otherwise create file
            # Load existing data from the JSON file
            with open(self.watchlist, 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            # If the file does not exist, initialize an empty list
            data = []

        # Add the new stock ticker entry
        data.append(stockticker)
        new_entry = {'symbol': stockticker[0], 'shortName': stockticker[1]}

        # Save the updated data back to the JSON file
        with open(self.watchlist, 'w') as file:
            json.dump(data, file, indent=4)

    # Usage
    file_path = 'watchlist.json'
    stockticker = "AAPL"
    add_stockticker_to_watchlist(file_path, stockticker)