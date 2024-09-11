from model.model import Model
import matplotlib.pyplot as plt
from view.mainview import Mainview
from model.tickerwrapper import TickerWrapper

class Graphicview:
    def __init__(self, model: Model, mainview: Mainview):
        self.model = model
        self.mainview = mainview

    #TODO: change self.model.tickerwrappers to symbollist, because we want to analyze only those, where hook is set at checkbox
    def initstaticGraph(self, symbollist: list, period: str) -> None:
        for tickerwrapper in self.model.tickerwrappers.values():
            tickerwrapper: TickerWrapper
            if not tickerwrapper.ticker.info["symbol"] in symbollist:
                #print("stocksymbol not in selected list for analysis")
                continue
            tickerhistory = tickerwrapper.tickerhistory["current"]
            #tickerhistory = tickerwrapper.ticker.history(period = period, interval = interval, prepost=True)
            tickerhistory['Close'].plot(label=f'{tickerwrapper.ticker.info["shortName"]}')
            if len(self.model.methods) == 0:
                #print("no method selected in analysis. Only stockdata will be printed")
                self.printGraph()
                continue
            # TODO: find more generic solution than accessing each[1] for statmethod, also its harcoded for Moving average method
            for value in self.model.methods.values():
                methodArgs = [int(each) for each in value]
            methods = [tickerhistory['Close'].rolling(window=methodArg).mean() for methodArg in methodArgs]
            for i, ma in enumerate(methods):
                ma.plot(label=f'{tickerwrapper.ticker.info["shortName"]} - Moving average: {methodArgs[i]}')
            self.printGraph()


    def printGraph(self) -> None:
        plt.title('Stock data')
        plt.legend()
        plt.show()