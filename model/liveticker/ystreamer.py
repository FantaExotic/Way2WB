from PySide6.QtCore import QThread, Signal
import websocket
from .yaticker_pb2 import yaticker
import base64
import json

class WebSocketWorker(QThread):
    message_received = Signal(dict)

    def __init__(self, tickers, ws_app, pb, reconnect=5):
        super().__init__()
        self.tickers = tickers
        self.ws_app = ws_app
        self.pb = pb
        self.reconnect = reconnect

    def run(self):
        self.ws_app.run_forever(reconnect=self.reconnect)

    def on_message(self, ws, message):
        message_bytes = base64.b64decode(message)
        self.pb.ParseFromString(message_bytes)

        data = {
            "id": self.pb.id,
            "exchange": self.pb.exchange,
            "quoteType": self.pb.quoteType,
            "price": self.pb.price,
            "timestamp": self.pb.time,
            "marketHours": self.pb.marketHours,
            "changePercent": self.pb.changePercent,
            "dayVolume": self.pb.dayVolume,
            "change": self.pb.change,
            "priceHint": self.pb.priceHint
        }

        # Emit the data as a signal
        self.message_received.emit(data)

class YahooStreamer:
    def __init__(self, tickers, bar_update_callback):
        self.tickers = tickers
        self.bar_update_callback = bar_update_callback
        self.pb = yaticker()

        # Set up the WebSocketApp with custom handlers
        self.ws = websocket.WebSocketApp(
            "wss://streamer.finance.yahoo.com/",
            on_message=lambda ws, msg: self.worker.on_message(ws, msg),
            on_open=lambda ws: self.on_open(ws),
        )

        # Create an instance of WebSocketWorker but don't start it yet
        self.worker = WebSocketWorker(self.tickers, self.ws, self.pb)

        # Connect the worker's signal to the callback
        self.worker.message_received.connect(self.bar_update_callback)

    def start(self, threaded=True, reconnect=5):
        if threaded:
            self.worker.reconnect = reconnect
            self.worker.start()
            # Set the thread to the lowest priority
            self.worker.setPriority(QThread.LowestPriority)
        else:
            self.worker.run()

    def stop(self):
        self.ws.close()
        self.worker.quit()
        self.worker.wait()

    def on_open(self, ws):
        ws.send(json.dumps({"subscribe": self.tickers}))

    def add_liveticker(self, ticker):
        self.ws.send(json.dumps({"subscribe": [ticker]}))
        self.tickers.append(ticker)

    def remove_liveticker(self, ticker):
        self.ws.send(json.dumps({"unsubscribe": [ticker]}))
        self.tickers.remove(ticker)