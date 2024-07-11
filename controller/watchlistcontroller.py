from model import Model
from view.view import View

class Watchlistcontroller:
    def __init__(self, model: Model, view: View):
        self.view = view
        self.model = model
        self.frame = self.view.watchlistview
        self.bind_view_controller()
        #self.bind_symbolentry_enterpressed()
        #self.bind_buttonDelete_listbox()
        #self.initWatchlistAndListbox()

    #def initWatchlistAndListbox(self):
    #    self.model.initWatchlist()
    #    self.view.initListbox(self.model)

    def bind_view_controller(self):
        self.view.watchlistview.button_return.configure(command=self.handle_buttonReturn)

    def handle_buttonReturn(self):
        self.view.setMainview()

    #def handle_entry_appendWatchlist(self):
    #    ticker = self.model.findTicker(self.view.watchlistview.symbol_var.get())
    #    symbol,shortname = ticker
    #    if symbol:
    #        #return symbol and shortname if found, "" else
    #        ret = self.model.add_stockticker_to_watchlist(ticker)
    #        if ret:
    #            self.view.addListboxElement(ticker)
#
    #def bind_symbolentry_enterpressed(self):
    #    self.view.watchlistview.enterbutton.configure(command=self.handle_entry_appendWatchlist)
#
    #def bind_buttonDelete_listbox(self):
    #    self.view.watchlistview.button_delete.configure(command=self.handle_buttonDelete)
#
    #def handle_buttonDelete(self):
    #    symbol = self.view.deleteListboxElement() # returnvalue is symbol of removed element
    #    #TODO: remove data from model
    #    del self.model.stockdata[symbol]
    #    for key,value in self.model.shortname.items():  #  workaround to ensure shortname and stockdata are consistent, but its in theory not necessary
    #        if key == symbol:
    #            del self.model.shortname[symbol]
    #            break
    #    self.model.remove_stockticker_from_watchlist(symbol)