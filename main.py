import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
import yfinance as yf
import matplotlib.pyplot as plt

class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Graph Generator")

        # Initialize variables
        self.data = None
        self.ticker = None
        self.movingAverage = None
        self.start_date_var = tk.StringVar(self)
        self.end_date_var = tk.StringVar(self)
        self.symbol_var = tk.StringVar(self)
        self.ma_entry = [ttk.Entry(self)]

        # Create widgets
        start_label = ttk.Label(self, text="Start Date:")
        start_label.grid(row=0, column=0, padx=5, pady=5)
        self.start_date_entry = DateEntry(self, textvariable=self.start_date_var, width=12, background='darkblue',
                                          foreground='white', borderwidth=2, date_pattern='y-mm-dd')
        self.start_date_entry.grid(row=0, column=1, padx=5, pady=5)

        end_label = ttk.Label(self, text="End Date:")
        end_label.grid(row=1, column=0, padx=5, pady=5)
        self.end_date_entry = DateEntry(self, textvariable=self.end_date_var, width=12, background='darkblue',
                                        foreground='white', borderwidth=2, date_pattern='y-mm-dd')
        self.end_date_entry.grid(row=1, column=1, padx=5, pady=5)

        symbol_label = ttk.Label(self, text="Enter Symbol:")
        symbol_label.grid(row=2, column=0, padx=5, pady=5)
        self.symbol_entry = ttk.Entry(self, textvariable=self.symbol_var)
        self.symbol_entry.grid(row=2, column=1, padx=5, pady=5)

        self.generate_data_button = ttk.Button(self, text="Generate Data", command=self.generate_data)
        self.generate_data_button.grid(row=0, column=3, padx=5, pady=5, sticky="ne")

        self.update_gui_button = ttk.Button(self, text="Update GUI", command=self.update_gui)
        self.update_gui_button.grid(row=1, column=3, padx=5, pady=5, sticky="ne")

        self.symbol_info_label = ttk.Label(self, text="Symbol input found: False\nShortname:\nSymbol:\nISIN:")
        self.symbol_info_label.grid(row=2, column=2, columnspan=2, padx=5, pady=5)

        ma_label = ttk.Label(self, text="Gleitender Durchschnitt:")
        ma_label.grid(row=3, column=0, padx=5, pady=5)

        # initialize first entry field for moving average
        self.ma_entry[0].grid(row=3, column=1, padx=5, pady=5)

        self.add_ma_button = ttk.Button(self, text="+", command=self.add_ma_entry)
        self.add_ma_button.grid(row=3, column=2, padx=5, pady=5)

        self.remove_ma_button = ttk.Button(self, text="-", command=self.remove_ma_entry)
        self.remove_ma_button.grid(row=3, column=3, padx=5, pady=5)

    def add_ma_entry(self):
        new_ma_entry = ttk.Entry(self)
        new_ma_entry.grid(row=len(self.ma_entry) + 3, column=1, padx=5, pady=5)
        self.ma_entry.append(new_ma_entry)

    def remove_ma_entry(self):
        if len(self.ma_entry) > 1:
            self.ma_entry[-1].destroy()
            self.ma_entry.pop()

    def generate_data(self):
        # Plot Close data
        self.data['Close'].plot(label='Close')
        movingAverageInput = [int(entry.get()) for entry in self.ma_entry]
        self.movingAverage = [self.data['Close'].rolling(window=entry).mean() for entry in movingAverageInput]
        
        # Plot Moving Averages with legends
        for i, ma in enumerate(self.movingAverage):
            ma.plot(label=f'MA {movingAverageInput[i]}')
        plt.title(self.ticker.info['shortName'])
        plt.legend()
        plt.show()

    def update_gui(self):
        start_date = self.start_date_var.get()
        end_date = self.end_date_var.get()
        symbol = self.symbol_var.get()

        # Update the start and end dates
        if symbol:
            try:
                self.data = yf.download(symbol, period="max")
                start_date = self.data.index[0].strftime('%Y-%m-%d')
                end_date = self.data.index[-1].strftime('%Y-%m-%d')

                self.ticker = yf.Ticker(symbol)
                short_name = self.ticker.info['shortName']
                symbol = self.ticker.info['symbol']
                isin = self.ticker.isin
                self.symbol_info_label.config(text=f"Symbol input found: True\nShortname: {short_name}\nSymbol: {symbol}\nISIN: {isin}")
            except Exception as e:
                self.symbol_info_label.config(text="Symbol input found: False")
                pass

        self.start_date_var.set(start_date)
        self.end_date_var.set(end_date)


if __name__ == "__main__":
    app = GUI()
    app.mainloop()
