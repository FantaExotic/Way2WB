from model.tickerwrapper import TickerWrapper

class CurrencyWrapper(TickerWrapper):
    """This class handles the currency conversion of all tickerwrappers to the desired currency (default: EURO)"""
    def __init__(self):
        super().__init__()
        self.currencydestination = "EUR"
        self.currencysource = None
        self.currencysymbol = None

    def convert_currency_in_tickerhistory(self, tickerwrapper: TickerWrapper):
        """Converts currency"""
        if not self.verify_conversion_preconditions_fullfilled(tickerwrapper=tickerwrapper):
            return tickerwrapper
        for interval in tickerwrapper.tickerhistory:
            if tickerwrapper.verify_tickerhistory_converted_already(currency_destination=self.currencydestination, interval=interval):
                continue
            tickerwrapper.tickerhistory[interval] = tickerwrapper.tickerhistory[interval] * self.get_conversionrate()
            tickerwrapper.tickerhistory_currency[interval] = self.currencydestination
        return tickerwrapper

    def verify_conversion_preconditions_fullfilled(self, tickerwrapper: TickerWrapper):
        if not tickerwrapper.verify_currency_conversion_required():
            return False
        if not self.verify_ticker_valid():
            return False
        return True
    
    def convert_currency_scalar(self, value: float):
        return value * self.get_conversionrate()
    
    def get_conversionrate(self):
        return self.ticker.fast_info["last_price"]