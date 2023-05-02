import datetime
import pytz

DEFAULT_TIMEZONE = pytz.timezone("US/Eastern")

def get_time():
    return datetime.datetime.now(DEFAULT_TIMEZONE).strftime("%Y-%m-%d %H:%M:%S ")
