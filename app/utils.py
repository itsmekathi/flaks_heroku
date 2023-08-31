from dateutil.relativedelta import relativedelta
from datetime import date
from flask import session
import pytz


def get_first_dateofthemonth():
    today = date.today()
    first_day = today.replace(day=1)
    # if today.day > 25:
    #     first_day = (first_day + relativedelta(months=1))
    # else:
    #     first_day = first_day
    return first_day

def get_local_date(value):
    '''Use timezone from the session object, if available, to localize datetimes from UTC.'''
    if 'timezone' not in session:
        return value

    # https://stackoverflow.com/a/34832184  
    utc_dt = pytz.utc.localize(value)
    local_tz = pytz.timezone(session['timezone'])
    local_dt = utc_dt.astimezone(local_tz)
    return local_dt