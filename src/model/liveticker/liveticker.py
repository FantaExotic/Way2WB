import pandas as pd
from model.currency import CurrencyWrapper
from model.tickerwrapper import TickerWrapper
import time
import warnings

class Liveticker:

    #TODO: do stresstest for livetickeranalysis (with many tickers). Are any updates missed?
    def __init__(self):
        self.timestamp_start = int(time.time())
        warnings.simplefilter(action='ignore', category=FutureWarning) #TODO shift this to settingsfile

    def append_liveticker_to_tickerwrapper(self, msg: dict, currencywrapper: CurrencyWrapper, tickerwrapper: TickerWrapper) -> None:
        """processes received data from liveticker and appends it to tickerhistory of corresponding ticker"""
        try:
            price = msg['price']
        except:
            print(f'No price was received in liveticker for {tickerwrapper.ticker.info_local["shortName"]}')
            return
        timestamp_ms = msg['time']
        timestamp_s = str(int(timestamp_ms) // 1000)  # Convert milliseconds to seconds

        if not self.verify_msg_valid(msg, timestamp=timestamp_s):
            return

        # convert currency if required
        if tickerwrapper.verify_currency_conversion_required():
            price = currencywrapper.convert_currency_scalar(price)

        new_value = {'Open': [price], 'High': [price], 'Low': [price], 'Close': [price], 'Volume': [-1], 'Dividends': [-1]}  # TODO: get volume and dividends data from liveticker (if possible)! 
        new_data = pd.DataFrame(new_value)
        new_data.index = pd.to_datetime([timestamp_s], unit="s")
        if new_data.index.tz is None:
            new_data.index = new_data.index.tz_localize("UTC")
        new_data.index = new_data.index.tz_convert(tickerwrapper.ticker._tz_local)
        new_data.index.name = tickerwrapper.tickerhistory['1m'].index.name
        # Update the existing tickerhistory['1m'] DataFrame with the new data
        new_dataframe = pd.concat([tickerwrapper.tickerhistory['1m'],new_data])
        tickerwrapper.tickerhistory['1m'] = new_dataframe

    def verify_msg_valid(self, msg: dict, timestamp: str):
        #TODO: create class to handle liveticker for each ticker individually. Update self.timestamp_start for each ticker individually!
        if int(timestamp) >= self.timestamp_start:
            return True
        #print(f'liveticker outdated invalid for {msg["id"]}')
        return False