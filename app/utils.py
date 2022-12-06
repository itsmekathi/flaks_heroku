from dateutil.relativedelta import relativedelta
from datetime import date


def get_first_dateofthemonth():
    today = date.today()
    first_day = today.replace(day=1)
    # if today.day > 25:
    #     first_day = (first_day + relativedelta(months=1))
    # else:
    #     first_day = first_day
    return first_day
