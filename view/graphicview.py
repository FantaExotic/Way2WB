from model import Model
import matplotlib.pyplot as plt
from view.mainview import Mainview

class Graphicview:
    def __init__(self, model, mainview, symbollist, period, interval):
        self.model = model
        self.mainview = mainview
        self.initstaticGraph(symbollist, period, interval)

    #TODO: change self.model.tickerlist to symbollist, because we want to analyze only those, where hook is set at checkbox
    def initstaticGraph(self, symbollist, period, interval):
        try:
            for stock in self.model.tickerlist:
                if (stock.info["symbol"] in symbollist):
                    tickerhistory = stock.history(period = period, interval = interval)
                    # TODO: find more generic solution than accessing each[1] for statmethod, also its harcoded for Moving average method
                    if len(self.model.methods) > 0:
                        movingAverageInput = [int(each[1]) for each in self.model.methods]
                        movingAverage = [tickerhistory['Close'].rolling(window=entry).mean() for entry in movingAverageInput]
                        for i, ma in enumerate(movingAverage):
                            ma.plot(label=f'{stock.info["shortName"]} - Moving average: {movingAverageInput[i]}')
                    tickerhistory['Close'].plot(label=f'{stock.info["shortName"]}')
            plt.title('Stock data')
            plt.legend()
            plt.show()
        except Exception as e:
            # Change appearance to show error
            print("Error! Graph could not be generated! Check the used methods and ensure its inputvalue is an integer!")
