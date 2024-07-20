import tkinter as tk
from tkcalendar import DateEntry

class Mainview(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.button_configWatchlist = tk.Button(self, text="Configure watchlist")
        self.button_configWatchlist.grid(row=1, column=3, padx=5, pady=5, sticky="ne")

        self.button_configAnalysis = tk.Button(self, text="Configure analysis")
        self.button_configAnalysis.grid(row=2, column=3, padx=5, pady=5, sticky="ne")

        self.button_generateGraph = tk.Button(self,text="Generate Graph")
        self.button_generateGraph.grid(row=3, column=3, padx=5, pady=5, sticky="ne")

    def create_mainview(self):
        pass

    def generate_data():
        pass

    def config_watchlist():
        pass

    def config_analysis():
        pass