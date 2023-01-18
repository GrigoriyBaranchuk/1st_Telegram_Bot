from logic_for_json import open_json, add_user_to_db, user_spreadsheetId
import telebot
from telebot import types
from logic import now_time, now_date, add_answers, generator
from logic_for_spreadsheet_API import create_table, upload_cell, check_is_full, table
import re
from datetime import datetime


bot = telebot.TeleBot('5973958816:AAHFvf3ql5SvVmyq1azrZcTRU5p8JwQtfLE')


@bot.message_handler(commands=['start', 'Назад'])
def start(message):
    """
    message.chat.id - chat identifier
    message.from_user.first_name - first name of user.
    We are able to take any information about user from message.from_user]
    """
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton('Добавить день'))


    first_name = message.from_user.first_name
    user_id = str(message.from_user.id)
    users_list = [inst['pk'] for inst in open_json()] #crate list of users pk from db
    if user_id not in users_list:
        spreadsheetId = create_table(name=first_name)
        to_json = {"pk": user_id, "first_name": first_name, "spreadsheetId": spreadsheetId}
        add_user_to_db(to_json)
        bot.send_message(message.chat.id, f'привет {first_name}', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, f'Привет {first_name} мы уже общались и у вас уже есть таблица'
                                          f' просто добавьте новый день',
                         reply_markup=markup)


@bot.message_handler(regexp='^[0-2][0-3]:[0-5][0-9]$')
def handle_time(message):
    if message.text.strip() == '11:22':
        new_var = datetime.strptime(message.text.strip(), '%H:%M').time()
        # import pdb
        # pdb.set_trace()
        pass


@bot.message_handler(content_types=['text'])
def handle_text(message):
    row = 2
    column = 1
    user_table = table(user_spreadsheetId(message))
    worksheet = user_table.get_worksheet(0)

    if message.text.strip() == 'Добавить день':
        if now_date() in user_table.get_worksheet(0).col_values(1):

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(types.KeyboardButton('Проснулся'))
            bot.send_message(message.chat.id, f'такая дата есть в таблице, добавить следующее действие', reply_markup=markup)
            pass
        else:
            while check_is_full(users_table=user_table.id, row=row, column=column):
                row += 1
            else:
                upload_cell(users_table=user_table.id, row=row, column=column, data=now_date())
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)


                markup.add(types.KeyboardButton('Проснулся'))
                markup.add(types.KeyboardButton('Добавить день'))
                bot.send_message(message.chat.id, f'добавить следующее действие', reply_markup=markup)

    elif message.text.strip() == 'Уснул':

        cell = generator(worksheet.findall("Уснул"))
        row = worksheet.find(str(now_date()))._row
        column = worksheet.find("Уснул").col

        while check_is_full(users_table=user_table.id, column=column, row=row):
            column = next(cell)._col

        else:
            upload_cell(users_table=user_table.id, row=row, column=column, data=now_time())
            bot.send_message(message.chat.id, f'малыш уснул в {now_time()}')
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

            markup.add(types.KeyboardButton('Проснулся'))
            markup.add(types.KeyboardButton('Добавить день'))
            bot.send_message(message.chat.id, f'добавить следующее действие', reply_markup=markup)

    elif message.text.strip() == 'Проснулся':


        cell = generator(worksheet.findall("Проснулся"))
        row = worksheet.find(str(now_date()))._row
        column = worksheet.find("Проснулся").col

        while check_is_full(users_table=user_table.id, column=column, row=row):
            column = next(cell)._col

        else:
            upload_cell(users_table=user_table.id, row=row, column=column, data=now_time())
            bot.send_message(message.chat.id, f'малыш проснулся в {now_time()}')


            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(types.KeyboardButton('Уснул'))
            markup.add(types.KeyboardButton('Добавить день'))
            bot.send_message(message.chat.id, f'добавить следующее действие', reply_markup=markup)





bot.polling(none_stop=True)
# TODO bot.webhook_listener - learn it

