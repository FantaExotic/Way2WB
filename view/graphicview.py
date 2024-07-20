import tkinter as tk
from model import Model
import matplotlib.pyplot as plt
import tkinter.messagebox as messagebox

class Graphicview:
    def __init__(self, model):
        self.initstaticGraph(model)

    def initstaticGraph(self,model):
        try:
            #TODO: fix graph generation
            if len(model.methods) > 0:
                movingAverageInput = [each for each in model.methods.values()]
                self.movingAverage = [model.data['Close'].rolling(window=entry).mean() for entry in movingAverageInput]
                # Plot Moving Averages with legends
                for i, ma in enumerate(self.movingAverage):
                    ma.plot(label=f'{self.ticker.info["symbol"]} - MA {movingAverageInput[i]}')
            model.stockdata['Close'].plot(label=f'{self.ticker.info["shortName"]} - ({self.ticker.info["symbol"]})')
            plt.title('Stock data')
            plt.legend()
            plt.show()
        except Exception as e:
            # Change appearance to show error
            messagebox.showerror("Error", "Graph could not be generated")