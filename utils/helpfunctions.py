################################################################################
## 
## helpfunction:
## get_keyFromDictValue
##
## Description:
## this helpfunction returns the key to the corresponding dict value
## 
################################################################################
#TODO: goes to mainview
def get_keyFromDictValue(value: str, dict: dict) -> str:
    key_list = list(dict.keys())
    val_list = list(dict.values())
    pos = val_list.index(value)
    return key_list[pos]

################################################################################
## 
## Helpfunction:
## setTickerArgs
##  
## Description:
## This function adjusts the argument interval for yf.Ticker call based 
## on the period argument, otherwise YFInvalidPeriodError will be thrown in
## scrapers/history.py
## Period/Interval relationship is hardcoded based on codesnipped from line 98-106
## 
################################################################################
#TODO: goes to class Period, which will be implemented in model
def setTickerArgs(period: str) -> str:
    if period in valid_period_1minute.keys():
        interval = "1m"
    elif period in valid_period_5minutes.keys():
        interval = "5m"
    elif period in valid_period_1hour.keys():
        interval = "1h"
    elif period in valid_period_1day.keys():
        interval = "1d"
    else:
        print("period not matching any element in self.valid_periods. default: interval = 1d")
        interval = "1d"
    return interval

#TODO: goes to class Interval, which will be implemented in model
def get_largest_period_for_same_interval(period: str) -> str:
    """Check which period class the input period belongs to, then return the last key, which is the largest one,
        if its written chronologically"""
    if period in valid_period_1minute:
        largest_period = list(valid_period_1minute.keys())[-1]
    elif period in valid_period_5minutes:
        largest_period = list(valid_period_5minutes.keys())[-1]
    elif period in valid_period_1hour:
        largest_period = list(valid_period_1hour.keys())[-1]
    elif period in valid_period_1day:
        largest_period = list(valid_period_1day.keys())[-1]
    else:
        print("error in assigning largest period for this periodclass")
        largest_period = "5d" # Default if the period is unmatched
    return largest_period


# helpvariables to determine interval based on period
valid_period_1minute = {"1d": "1 day", 
                           "5d": "5 days"}
valid_period_5minutes = {"1mo": "1 month"}
valid_period_1hour = {"3mo": "3 months",
                       "6mo": "6 months",
                       "1y": "1 year",
                       "2y": "2 years",}
valid_period_1day = {"5y": "5 years",
                       "10y": "10 years",
                       "max": "Maximum period"}
valid_periods = valid_period_1minute | valid_period_5minutes | valid_period_1hour | valid_period_1day
