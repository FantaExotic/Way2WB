from model.tickerwrapper import TickerWrapper
from model.historymanager import *


class Rule:
    def __init__(self):
        self.threshold = None
        self.shortname = None
        self.symbol = None
        self.period = None
        self.activated = None

    def create_rule(self, threshold: int, shortname: str, symbol: str, period: Period_Tickerhistory, activated: bool):
        self.threshold = threshold
        self.shortname = shortname
        self.symbol = symbol
        self.period = period
        self.activated = activated
