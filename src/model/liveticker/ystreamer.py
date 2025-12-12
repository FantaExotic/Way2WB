from PySide6.QtCore import QThread
import yfinance as yf

class YFStreamer(QThread):

    def __init__(self, tickers, callbackfunction, liveticker_enabled: bool) -> None:
        super().__init__()
        #self.setObjectName("Liveticker_main_thread")
        self.yfWebsocket = None
        self.callbackfunction = callbackfunction
        self.initTickers = tickers
        self.liveticker_enabled = liveticker_enabled

    def start_YFStreamer(self):
        if self.liveticker_enabled:
            self.yfWebsocket = yf.WebSocket()
            self.initSubscriptions()
            self.start()

    def initSubscriptions(self):
        for ticker in self.initTickers:
            self.add_liveticker(ticker)

    def stop(self):
        self.yfWebsocket.close()

    def add_liveticker(self, ticker):
        if self.liveticker_enabled: self.yfWebsocket.subscribe(ticker)

    def remove_liveticker(self, ticker):
        if self.liveticker_enabled: self.yfWebsocket.unsubscribe(ticker)

    def run(self):
        self.yfWebsocket.listen(message_handler=self.callbackfunction)
        #self.setPriority(QThread.LowestPriority)