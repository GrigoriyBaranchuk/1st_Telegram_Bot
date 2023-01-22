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


def add_answers(bot, message):
    """answers for button"""

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton('Уснул'))
    markup.add(types.KeyboardButton('Проснулся'))
    markup.add(types.KeyboardButton('Добавить день'))
    bot.send_message(message.chat.id, f'добавить следующее действие', reply_markup=markup)


def generator(iter):
    for i in iter:
        yield i

