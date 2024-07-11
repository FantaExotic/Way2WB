from model import Model
from view.view import View
from controller.maincontroller import Maincontroller
from controller.watchlistcontroller import Watchlistcontroller
from controller.analysiscontroller import Analysiscontroller

class Controller:
    def __init__(self, model: Model, view: View) -> None:
        self.model = model
        self.view = view
        self.maincontroller = Maincontroller(model=model, view=view)
        self.watchlistcontroller = Watchlistcontroller(model=model, view=view)
        self.analysiscontroller = Analysiscontroller(model=model, view=view)
        self.initWatchlistAndListbox()
        self.bind_symbolentry_enterpressed()
        self.bind_buttonDelete_listbox()

    def run(self) -> None:
        self.view.root.mainloop()

    def initWatchlistAndListbox(self):
        self.model.initWatchlist()
        self.view.initListbox(self.model)

    def handle_entry_appendWatchlist(self):
        ticker = self.model.findTicker(self.view.watchlistview.symbol_var.get())
        symbol,shortname = ticker
        if symbol:
            #return symbol and shortname if found, "" else
            ret = self.model.add_stockticker_to_watchlist(ticker)
            if ret:
                self.view.addListboxElement(ticker)

    def handle_buttonDelete(self):
        symbol = self.view.deleteListboxElement() # returnvalue is symbol of removed element
        #TODO: remove data from model
        del self.model.stockdata[symbol]
        for key,value in self.model.shortname.items():  #  workaround to ensure shortname and stockdata are consistent, but its in theory not necessary
            if key == symbol:
                del self.model.shortname[symbol]
                break
        self.model.remove_stockticker_from_watchlist(symbol)

    def bind_symbolentry_enterpressed(self):
        self.view.watchlistview.enterbutton.configure(command=self.handle_entry_appendWatchlist)

    def bind_buttonDelete_listbox(self):
        self.view.watchlistview.button_delete.configure(command=self.handle_buttonDelete)