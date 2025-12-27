from PySide6.QtCore import QThread
import yfinance as yf
from PySide6 import QtAsyncio
import time

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

    def initSubscriptions(self):
        for ticker in self.initTickers:
            self.yfWebsocket.subscribe(ticker)

    def stop(self):
        self.yfWebsocket.close()

    def add_liveticker(self, ticker):
        if self.liveticker_enabled: 
            self.yfWebsocket.subscribe(ticker)
            self.initTickers.append(ticker)

    def remove_liveticker(self, ticker):
        if self.liveticker_enabled: 
            self.yfWebsocket.unsubscribe(ticker)
            self.initTickers.remove(ticker)

    def run(self):
        #self.setPriority(QThread.LowestPriority)
        while True:
            #prepare websocket if disconnected
            try:
                self.start_YFStreamer()
                self.yfWebsocket.listen(message_handler=self.callbackfunction)
                print("yfWebsocket closed. Restarting listener")
            except:
                print("yfWebsocket disconnected. Restarting listener")
            finally:
                print("waiting before reconnect ...")
                time.sleep(10)
                print("restart reconnect")