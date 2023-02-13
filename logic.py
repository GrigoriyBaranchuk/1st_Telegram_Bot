from datetime import datetime
import pytz


def now_time():
    """return time at the current moment"""
    return datetime.now(pytz.timezone('Europe/Moscow')).strftime('%H:%M')


def now_date():
    """return time at the current moment"""
    return datetime.now(pytz.timezone('Europe/Moscow')).strftime('%d-%m-%Y')
# TODO change function  to create tim of user not server or some utc


def generator(iter):
    for i in iter:
        yield i


def multi_replase(string, replace_value=[':', ';', '/', '.', '_', '-', ',']):
    """function to bringing time(11.20 or 11,20) from user message  to HH:MM form """
    for val in replace_value:
        string = string.replace(val, ':')
        if string.count(':') > 1:
            string = string.replace(':', '')

    return string