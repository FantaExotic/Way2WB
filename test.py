import yliveticker as ylt
import json


# this function is called on each ticker update
def on_new_msg(ws, msg):
    print(f'received message: {msg}')
    print(f'first dict entry: {msg['id']}')
    print(f'second dict entry: {msg['price']}')



liveticker = ylt.YLiveTicker(on_ticker=on_new_msg, ticker_names=[
    "BTC-USD", "AAPL", "DTE.DE", "MSFT"])
