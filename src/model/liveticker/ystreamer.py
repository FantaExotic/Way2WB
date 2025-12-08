from PySide6.QtCore import QThread, Signal
import yfinance as yf

class YFStreamer(QThread):

    def __init__(self, tickers, callbackfunction):
        super().__init__()
        self.yfWebsocket = yf.WebSocket()
        self.callbackfunction = callbackfunction
        for ticker in tickers:
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