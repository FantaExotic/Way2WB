import tkinter as tk
from tkcalendar import DateEntry

class Watchlistview(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=10)  # more weight to row with Listbox
        
        self.button_return = tk.Button(self, text="X")
        self.button_return.grid(row=0, column=2, padx=5, pady=5, sticky="ne")

        self.label = tk.Label(self, text="Stock Symbol found: False\nShortname:\nSymbol:\nISIN:")
        self.label.grid(row=0, column=0, padx=5, pady=5, sticky="ne")

        self.list = tk.Listbox(self)
        self.list.grid(row=3, column=0, padx=15, pady=15, sticky="nsew")
        
        self.symbol_var = tk.StringVar(self)
        self.symbol_entry = tk.Entry(self, textvariable=self.symbol_var)
        self.symbol_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ne")


    def add_ma_entry(self):
        pass

    def remove_ma_entry(self):
        pass

    def add_ma_entry():
        pass

    def remove_ma_entry():
        pass

    def appendWatchlist(self):
        