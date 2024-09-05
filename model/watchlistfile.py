import os
from pathlib import Path
import json

class Watchlistfile:

    def __init__(self):
        self.basepath = Path(__file__).resolve().parent
        self.watchlistfilePath = self.basepath.joinpath("watchlist.json")  # configfile containing watchlist

    def check_watchlistfile(self) -> bool:
        """Checks if watchlistfile exists and contains data"""
        if not os.path.exists(self.watchlistfilePath):
            print("Watchlistfile not found!")
            Path(self.watchlistfilePath).touch()
            return False
        if not os.path.getsize(self.watchlistfilePath)>0:
            print("Watchlistfile is empty!")
            return False
        return True

    def remove_ticker_from_watchlistfile(self, symbol: str) -> None:
        """Removes ticker from watchlistfile based on symbol in arg"""
        check = self.check_watchlistfile()
        if not check:
            return
        with open(self.watchlistfilePath, 'r') as file:
            data = json.load(file)
        # extract each[0] (symbol) from each element in data, to check for duplicates
        tmpdata = [each[0] for each in data]
        for index,each in enumerate(tmpdata):
            if each == symbol:
                data.pop(index)
        with open(self.watchlistfilePath, 'w') as file:
            json.dump(data, file, indent=4)

    def check_duplicates_in_watchlistfile(self,symbol: str) -> bool:
        """Cheks if symbol in arg is duplicate in watchlistfile """
        with open(self.watchlistfilePath, 'r') as file:
            data = json.load(file)
        # extract each[0] (symbol) from each element in data, to check for duplicates
        tmpdata = [each[0] for each in data]
        if symbol in tmpdata:
            print("Stock already exists in Watchlistfile!")
            return True
        else:
            return False

    def add_tickerinfo_to_watchlistfile(self, symbol: str, shortName: str) -> None:
        """Adds symbol and shortName of ticker to watchlistfile"""
        if not self.check_watchlistfile():
            return
        with open(self.watchlistfilePath, 'r') as file:
            data = json.load(file)
        data.append([symbol, shortName])
        with open(self.watchlistfilePath, 'w') as file:
            json.dump(data, file, indent=4)