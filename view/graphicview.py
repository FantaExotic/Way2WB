import tkinter as tk
from model import Model
import matplotlib.pyplot as plt
import tkinter.messagebox as messagebox

class Graphicview:
    def __init__(self, model, analysisview):
        self.initstaticGraph(model, analysisview)

    def initstaticGraph(self,model,analysisview):
        try:
            selected_items = analysisview.listbox.get_checked()
            selected_stocks = []
            for item in selected_items:
                selected_text = analysisview.listbox.item(item, "text")
                symbol = selected_text.split(" ")[0]
                selected_stocks.append(symbol)
            for stock in selected_stocks:
                if len(model.methods) > 0:
                    movingAverageInput = [each['value'] for each in model.methods]
                    movingAverage = [model.stockdata[stock]['Close'].rolling(window=entry).mean() for entry in movingAverageInput]
                    for i, ma in enumerate(movingAverage):
                        ma.plot(label=f'{model.shortname[stock]} - Moving average: {movingAverageInput[i]}')
                model.stockdata[stock]['Close'].plot(label=f'{model.shortname[stock]}')
            plt.title('Stock data')
            plt.legend()
            plt.show()
        except Exception as e:
            # Change appearance to show error
            messagebox.showerror("Error", "Graph could not be generated")