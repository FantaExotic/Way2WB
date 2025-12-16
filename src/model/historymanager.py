from enum import Enum

#TODO: currently the possible period and intervals are hardcoded. Analyse if those infos can be parsed from the tickers!

class Interval_Tickerhistory(Enum):
    MINUTE_1 = "1m"
    MINUTES_5 = "5m"
    HOUR_1 = "1h"
    DAY_1 = "1d"

class Period_Tickerhistory(Enum):
    DAY_1 = "1d"
    DAYS_5 = "5d"
    MONTH_1 = "1mo"
    MONTHS_3 = "3mo"
    MONTHS_6 = "6mo"
    YEAR_1 = "1y"
    YEARS_2 = "2y"
    YEARS_5 = "5y"
    YEARS_10 = "10y"
    MAX = "max"

class Period_Tickerhistory_Longname(Enum):
    """Longenum is needed for combobox_period to map longname to shortname"""
    DAY_1 = "1 day"
    DAYS_5 = "5 days"
    MONTH_1 = "1 month"
    MONTHS_3 = "3 months"
    MONTHS_6 = "6 months"
    YEAR_1 = "1 year"
    YEARS_2 = "2 years"
    YEARS_5 = "5 years"
    YEARS_10 = "10 years"
    MAX = "Maximum period"

def get_largest_period_for_same_interval(period: Period_Tickerhistory) -> Period_Tickerhistory:
    if period == Period_Tickerhistory.DAY_1.value:
        return Period_Tickerhistory.DAYS_5.value
    elif (period == Period_Tickerhistory.MONTHS_3.value or
            period == Period_Tickerhistory.MONTHS_6.value or 
            period == Period_Tickerhistory.YEAR_1.value):
        return Period_Tickerhistory.YEARS_2.value
    elif (period == Period_Tickerhistory.YEARS_5.value or
            period == Period_Tickerhistory.YEARS_10.value):
        return Period_Tickerhistory.MAX.value
    else:
        return period

def assign_period_to_interval(period: Period_Tickerhistory) -> Interval_Tickerhistory:
    if (period == Period_Tickerhistory.DAY_1.value or 
        period == Period_Tickerhistory.DAYS_5.value):
        return Interval_Tickerhistory.MINUTE_1.value
    elif period == Period_Tickerhistory.MONTH_1.value:
        return Interval_Tickerhistory.MINUTES_5.value
    elif (period == Period_Tickerhistory.MONTHS_3.value or
            period == Period_Tickerhistory.MONTHS_6.value or 
            period == Period_Tickerhistory.YEAR_1.value or
            period == Period_Tickerhistory.YEARS_2.value):
        return Interval_Tickerhistory.HOUR_1.value
    elif (period == Period_Tickerhistory.YEARS_5.value or
            period == Period_Tickerhistory.YEARS_10.value or 
            period == Period_Tickerhistory.MAX.value):
        return Interval_Tickerhistory.DAY_1.value
    

def get_shortname_from_longname(longname: Period_Tickerhistory_Longname) -> Period_Tickerhistory:
    """Returns the enum member based on the provided value"""
    for period_longname in Period_Tickerhistory_Longname:
        if period_longname.value == longname:
            return Period_Tickerhistory[period_longname.name].value
    return Period_Tickerhistory.DAYS_5.value  # default value