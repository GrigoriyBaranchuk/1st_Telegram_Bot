from datetime import datetime
import pytz
from telebot import types


def now_time():
    """return time at the current moment in str"""
    return datetime.now(pytz.timezone('Europe/Moscow')).strftime('%H:%M')


def now_date():
    """return time at the current moment in str"""
    return datetime.now(pytz.timezone('Europe/Moscow')).strftime('%d-%m-%Y')
# TODO change function  to create tim of user not server or some utc


def generator(iter):
    for i in iter:
        yield i

