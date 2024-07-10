from model import Model
from view.root import Root
from view.mainview import Mainview
from view.watchlistview import Watchlistview

class View:
    def __init__(self, model: Model) -> None:
        self.root = Root()
        self.mainview = Mainview(self.root)
        self.watchlistview = Watchlistview(self.root)
        self.currentview = self.mainview
        self.setMainview()

    def setMainview(self):
        if self.currentview is not None:
            self.currentview.grid_forget()
        self.currentview = self.mainview
        self.currentview.grid(row=0, column=0, sticky="nsew")

    def setWatchlistview(self):
        if self.currentview is not None:
            self.currentview.grid_forget()
        self.currentview = self.watchlistview
        self.currentview.grid(row=0, column=0, sticky="nsew")

    def currentview(self):
        pass

    def create_mainview(self):
        pass

    def generate_data():
        pass

    def config_watchlist():
        pass

    def config_analysis():
        pass

