from PySide6.QtCore import QThread
import yfinance as yf

class YFStreamer(QThread):

    def __init__(self, tickers, callbackfunction):
        super().__init__()
        #self.setObjectName("Liveticker_main_thread")
        self.yfWebsocket = yf.WebSocket()
        self.callbackfunction = callbackfunction
        self.initTickers = tickers
        self.initSubscriptions()

    def initSubscriptions(self):
        for ticker in self.initTickers:
            self.add_liveticker(ticker)

    def stop(self):
        self.yfWebsocket.close()

    def add_liveticker(self, ticker):
        self.yfWebsocket.subscribe(ticker)

    def remove_liveticker(self, ticker):
        self.yfWebsocket.unsubscribe(ticker)

    def run(self):
        self.yfWebsocket.listen(message_handler=self.callbackfunction)
        #self.setPriority(QThread.LowestPriority)