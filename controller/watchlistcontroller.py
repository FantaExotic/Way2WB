from model import Model
from view.view import View

class Watchlistcontroller:
    def __init__(self, model: Model, view: View):
        self.view = view
        self.model = model
        self.frame = self.view.watchlistview
        self.bind_view_controller()
        self.bind_symbolentry_enterpressed()
        self.initWatchlistAndListbox()

    def initWatchlistAndListbox(self):
        self.model.initWatchlist()
        self.view.watchlistview.initListbox(self.model)

    def bind_view_controller(self):
        self.view.watchlistview.button_return.configure(command=self.handle_buttonReturn)

    def handle_buttonReturn(self):
        self.view.setMainview()

    def handle_entry_appendWatchlist(self):
        ticker = self.model.findTicker(self.view.watchlistview.symbol_var.get())
        if ticker:
            #return value 1 = added to watchlistfile, 0 else
            ret = self.model.add_stockticker_to_watchlist(ticker)
            if ret:
                self.view.watchlistview.appendListbox(ticker)

    def bind_symbolentry_enterpressed(self):
        self.view.watchlistview.enterbutton.configure(command=self.handle_entry_appendWatchlist)