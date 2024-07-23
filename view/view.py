import tkinter as tk
from model import Model
from view.root import Root
from view.mainview import Mainview
from view.watchlistview import Watchlistview
from view.analysisview import Analysisview
from view.graphicview import Graphicview

class View:
    def __init__(self, model: Model) -> None:
        self.root = Root()
        self.model = model
        self.mainview = Mainview(self.root)
        self.watchlistview = Watchlistview(self.root)
        self.analysisview = Analysisview(self.root)
        #self.graphicview = Graphicview(self.root)
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

    def setAnalysisview(self):
        if self.currentview is not None:
            self.currentview.grid_forget()
        self.currentview = self.analysisview
        self.currentview.grid(row=0, column=0, sticky="nsew")

    def setGraphview(self):
        plotgraph = Graphicview(self.model, self.analysisview)

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

    def addListboxElement(self,ticker):
        temp = ' '.join(ticker)
        self.watchlistview.listbox.insert(tk.END,temp)
        self.watchlistview.symbol_entry.delete(0,"end")
        self.analysisview.listbox.insert('', 'end',text=temp)

    #TODO: write generic function for adding listbox element
    def initListbox(self,model):
        for each in model.stockdata.keys():
            temp = f'{each} {model.shortname[each]}'
            self.watchlistview.listbox.insert(tk.END,temp)
            self.analysisview.listbox.insert('', 'end',text=temp)

    def deleteListboxElement(self):
        selected_element = self.watchlistview.listbox.curselection()[0]
        selected_text = self.watchlistview.listbox.get(selected_element)
        symbol = selected_text.split(" ")[0]
        self.watchlistview.listbox.delete(selected_element)
        #childindex required because delete(index) isnt working with CheckboxTreeview
        childIndex = self.analysisview.listbox.get_children()[selected_element]
        self.analysisview.listbox.delete(childIndex)
        return symbol