from model.tickerwrapper import TickerWrapper
from model.historymanager import *
from model.notifier.notifier import Notifier

class Rule_Types(Enum):
    PCT_UPPERTHRESHOLD = "Percentage Upper Threshold"
    PCT_LOWERRTHRESHOLD = "Percentage Lower Threshold"
    ABS_UPPERTHRESHOLD = "Absolute Upper Threshold"
    ABS_LOWERTHRESHOLD = "Absolute Lower Threshold"

class Rule:
    def __init__(self):
        self.threshold = None
        self.tickerwrapper: TickerWrapper | None = None
        self.period = None
        self.activated = True   #TODO: implement dynamic activation of each rule in table rule
        self.ruletype: Rule_Types | None = None

    #TODO: remove create_rule, and shift the function logic to __init__
    def create_rule(self, threshold: int, tickerwrapper:TickerWrapper, period: Period_Tickerhistory, ruletype: Rule_Types) -> None:
        self.threshold = threshold
        self.tickerwrapper = tickerwrapper
        self.period = period
        self.ruletype = ruletype

    def check_rule_pct_upperthreshold(self) -> bool:
        """checks if rule percentage is fulfilled for given period"""
        period_shortname = get_shortname_from_longname(self.period)
        interval = assign_period_to_interval(period_shortname)
        currentprice = self.tickerwrapper.tickerhistory[interval]['Open'].values[-1].item()
        # Get 'Close' prices for the current ticker
        startprice = self.tickerwrapper.tickerhistory[interval]['Close'].iloc[0]
        return (currentprice/startprice-1)*100 >= self.threshold

    def check_rule_pct_lowerthreshold(self) -> bool:
        """checks if rule percentage is fulfilled for given period"""
        period_shortname = get_shortname_from_longname(self.period)
        interval = assign_period_to_interval(period_shortname)
        currentprice = self.tickerwrapper.tickerhistory[interval]['Open'].values[-1].item()
        # Get 'Close' prices for the current ticker
        startprice = self.tickerwrapper.tickerhistory[interval]['Close'].iloc[0]
        return(currentprice/startprice-1)*100 <= -self.threshold

    def check_rule_abs_upperthreshold(self) -> bool:
        """checks if rule absolute is fulfilled for given tickerwrapper"""
        period_shortname = get_shortname_from_longname(self.period)
        interval = assign_period_to_interval(period_shortname)
        currentprice = self.tickerwrapper.tickerhistory[interval]['Open'].values[-1].item()
        return currentprice >= self.threshold

    def check_rule_abs_lowerthreshold(self) -> bool:
        """checks if rule absolute is fulfilled for given tickerwrapper"""
        period_shortname = get_shortname_from_longname(self.period)
        interval = assign_period_to_interval(period_shortname)
        currentprice = self.tickerwrapper.tickerhistory[interval]['Open'].values[-1].item()
        return currentprice <= self.threshold


class Rules:
    def __init__(self):
        self.rules = dict()
        self.notifier = Notifier()
        self.enable_default = None

    def add_to_rules(self, rule: Rule, symbol: str) -> None:
        self.rules[symbol].append(rule) #TODO: check if values self.rules[symbol]= list() shall be declared

    def get_rule(self,symbol: str, index: int) -> Rule:
        return self.rules[symbol][index]
    
    def is_rule_unique(self, symbol: str, threshold: int, period: Period_Tickerhistory, ruletype: Rule_Types) -> bool:
        if not symbol in self.rules:
            self.rules[symbol] = list()
            return True
        for rule in self.rules[symbol]:
            rule: Rule
            if not rule.period == period:
                continue
            if not rule.threshold == threshold:
                continue
            if not rule.ruletype == ruletype:
                continue
            return False
        return True


    def check_rules(self, symbol: str) -> None:
        if not symbol in self.rules:
            return
        for rule in self.rules[symbol]:
            rule: Rule
            if rule.activated:
                if rule.ruletype == Rule_Types.PCT_UPPERTHRESHOLD.value:
                    if rule.check_rule_pct_upperthreshold():
                        print(f'Rule triggered: {rule.tickerwrapper.ticker.info_local["symbol"]} exceeded percentage upper threshold of {rule.threshold}% for period {rule.period}')
                        self.notifier.send_notification(message=f'Rule triggered: {rule.tickerwrapper.ticker.info_local["shortName"]} exceeded percentage upper threshold of {rule.threshold}% for period {rule.period}')
                if rule.ruletype == Rule_Types.PCT_LOWERRTHRESHOLD.value:
                    if rule.check_rule_pct_lowerthreshold():
                        print(f'Rule triggered: {rule.tickerwrapper.ticker.info_local["symbol"]} exceeded percentage lower threshold of {rule.threshold}% for period {rule.period}')
                        self.notifier.send_notification(message=f'Rule triggered: {rule.tickerwrapper.ticker.info_local["shortName"]} exceeded percentage lower threshold of {rule.threshold}% for period {rule.period}')
                if rule.ruletype == Rule_Types.ABS_UPPERTHRESHOLD.value:
                    if rule.check_rule_abs_upperthreshold():
                        print(f'Rule triggered: {rule.tickerwrapper.ticker.info_local["symbol"]} exceeded absolute upper threshold of {rule.threshold} for period {rule.period}')
                        self.notifier.send_notification(message=f'Rule triggered: {rule.tickerwrapper.ticker.info_local["shortName"]} exceeded absolute upper threshold of {rule.threshold} for period {rule.period}')
                if rule.ruletype == Rule_Types.ABS_LOWERTHRESHOLD.value:
                    if rule.check_rule_abs_lowerthreshold():
                        print(f'Rule triggered: {rule.tickerwrapper.ticker.info_local["symbol"]} exceeded absolute lower threshold of {rule.threshold} for period {rule.period}')
                        self.notifier.send_notification(message=f'Rule triggered: {rule.tickerwrapper.ticker.info_local["shortName"]} exceeded absolute lower threshold of {rule.threshold} for period {rule.period}')
            rule.activated = False #TODO: workaround to trigger notifier only once, because deactivating rule via GUI is currently not possible