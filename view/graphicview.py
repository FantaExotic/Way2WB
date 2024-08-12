from model import Model
import matplotlib.pyplot as plt
from view.mainview import Mainview

class Graphicview:
    def __init__(self, model, mainview):
        self.model = model
        self.mainview = mainview

    #TODO: change self.model.tickerlist to symbollist, because we want to analyze only those, where hook is set at checkbox
    def initstaticGraph(self, symbollist, period, interval):
        for stock in self.model.tickerlist:
            if not stock.info["symbol"] in symbollist:
                #print("stocksymbol not in selected list for analysis")
                continue
            tickerhistory = stock.history(period = period, interval = interval)
            tickerhistory['Close'].plot(label=f'{stock.info["shortName"]}')
            if len(self.model.methods) == 0:
                #print("no method selected in analysis. Only stockdata will be printed")
                self.printGraph()
                continue
            # TODO: find more generic solution than accessing each[1] for statmethod, also its harcoded for Moving average method
            movingAverageInput = [int(each[1]) for each in self.model.methods]
            movingAverage = [tickerhistory['Close'].rolling(window=entry).mean() for entry in movingAverageInput]
            for i, ma in enumerate(movingAverage):
                ma.plot(label=f'{stock.info["shortName"]} - Moving average: {movingAverageInput[i]}')
            self.printGraph()

    def printGraph(self):
        plt.title('Stock data')
        plt.legend()
        plt.show()