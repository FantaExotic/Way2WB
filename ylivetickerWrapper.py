from PySide6.QtCore import QThread, Signal, QObject
import yliveticker as ylt

class YLiveTickerWorker(QObject):
    ticker_updated = Signal(dict)  # Signal to emit ticker updates

    def __init__(self, ticker_names):
        super().__init__()
        self.ticker_names = ticker_names
        self.is_running = True

    def on_livetickerMessage(self, ws, msg):
        # Emit the received message (this will be caught in the main thread)
        self.ticker_updated.emit(msg)

    def run(self):
        # Start the yliveticker and keep it running
        self.yliveticker = ylt.YLiveTicker(on_ticker=self.on_livetickerMessage, ticker_names=self.ticker_names)
        while self.is_running:
            self.yliveticker.ws.run_forever()

    def stop(self):
        self.is_running = False
        self.yliveticker.ws.close()