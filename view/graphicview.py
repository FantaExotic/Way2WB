from model.model import Model
import matplotlib.pyplot as plt
from view.mainview import Mainview
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime,  timedelta
from model.tickerwrapper import TickerWrapper

class Graphicview:
    def __init__(self, model, mainview):
        self.model = model
        self.mainview = mainview

    #TODO: change self.model.tickerlist to symbollist, because we want to analyze only those, where hook is set at checkbox
    def initstaticGraph(self, symbollist: list, period: str) -> None:
        for tickerwrapper in self.model.tickerlist:
            if not tickerwrapper.ticker.info["symbol"] in symbollist:
                #print("stocksymbol not in selected list for analysis")
                continue
            tickerhistory = tickerwrapper.get_tickerhistory(period = period)
            #tickerhistory = tickerwrapper.ticker.history(period = period, interval = interval, prepost=True)
            tickerhistory['Close'].plot(label=f'{tickerwrapper.ticker.info["shortName"]}')
            if len(self.model.methods) == 0:
                #print("no method selected in analysis. Only stockdata will be printed")
                self.printGraph()
                continue
            # TODO: find more generic solution than accessing each[1] for statmethod, also its harcoded for Moving average method
            movingAverageInput = [int(each[1]) for each in self.model.methods]
            movingAverage = [tickerhistory['Close'].rolling(window=entry).mean() for entry in movingAverageInput]
            for i, ma in enumerate(movingAverage):
                ma.plot(label=f'{tickerwrapper.ticker.info["shortName"]} - Moving average: {movingAverageInput[i]}')
            self.printGraph()


    def printGraph(self) -> None:
        plt.title('Stock data')
        plt.legend()
        plt.show()