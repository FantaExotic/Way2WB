import tkinter as tk
from tkcalendar import DateEntry

class Mainview(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.grid_columnconfigure(0, weight=1)
        #self.grid_rowconfigure(0, weight=1)

        #self.start_date_var = tk.StringVar(self)
        #self.end_date_var = tk.StringVar(self)

        #start_label = tk.Label(self, text="Start Date:")
        #start_label.grid(row=0, column=0, padx=5, pady=5)
        #self.start_date_entry = DateEntry(self, textvariable=self.start_date_var, width=12, background='darkblue',
        #                                  foreground='white', borderwidth=2, date_pattern='y-mm-dd')
        #self.start_date_entry.grid(row=0, column=1, padx=5, pady=5)

        #end_label = tk.Label(self, text="End Date:")
        #end_label.grid(row=1, column=0, padx=5, pady=5)
        #self.end_date_entry = DateEntry(self, textvariable=self.end_date_var, width=12, background='darkblue',
        #                                foreground='white', borderwidth=2, date_pattern='y-mm-dd')
        #self.end_date_entry.grid(row=1, column=1, padx=5, pady=5)

        #self.button_generateData = tk.Button(self, text="Generate Data", command=self.generate_data)
        #self.button_generateData.grid(row=0, column=3, padx=5, pady=5, sticky="ne")

        self.button_configWatchlist = tk.Button(self, text="Configure watchlist")
        self.button_configWatchlist.grid(row=1, column=3, padx=5, pady=5, sticky="ne")

        #self.button_configAnalysis = tk.Button(self, text="Configure analysis", command=self.config_analysis)
        #self.button_configAnalysis.grid(row=2, column=3, padx=5, pady=5, sticky="ne")

    def create_mainview(self):
        pass

    def generate_data():
        pass

    def config_watchlist():
        pass

    def config_analysis():
        pass