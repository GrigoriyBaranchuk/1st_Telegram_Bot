from logic_for_json import open_json, add_user_to_db, user_spreadsheetId
import telebot
from telebot import types
from logic import now_time, now_date, generator
from logic_for_spreadsheet_API import create_table, upload_cell, check_is_full, table, create_new_day
from datetime import datetime

import gspread


bot = telebot.TeleBot('5973958816:AAHFvf3ql5SvVmyq1azrZcTRU5p8JwQtfLE')
path = 'service_account.json'
gs = gspread.service_account(filename=path)


@bot.message_handler(commands=['start'])
def start(message):
    """
    message.chat.id - chat identifier
    message.from_user.first_name - first name of user.
    We are able to take any information about user from message.from_user]
    """
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton('Уснул'))
    markup.add(types.KeyboardButton('Проснулся'))

    first_name = message.from_user.first_name
    user_id = str(message.from_user.id)
    users_list = [inst['pk'] for inst in open_json()] #crate list of users pk from db
    if user_id not in users_list:
        spreadsheetId = create_table(gs=gs, name=first_name)
        to_json = {"pk": user_id, "first_name": first_name, "spreadsheetId": spreadsheetId}
        add_user_to_db(to_json)
        bot.send_message(message.chat.id, f'привет {first_name}', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, f'Привет {first_name} мы уже общались и у вас уже есть таблица'
                                          f' просто нажмите уснул малыш или проснулся',
                         reply_markup=markup)


@bot.message_handler(regexp='[А-яа-я]{5}\s[0-2][0-9]:[0-5][0-9]')
def handle_time(message):
    user_table = table(gs=gs, users_table=user_spreadsheetId(message))
    worksheet = user_table.get_worksheet(0)
    message_from_user = message.text.strip()
    # time_from_user = datetime.strptime(message_from_user.split(' ')[-1], '%H:%M').time()
    time_from_user = message_from_user.split(' ')[-1]
    action_from_user = message_from_user.split(' ')[0]

    # import pdb
    # pdb.set_trace()


    if action_from_user.lower() == 'уснул':
        create_new_day(gs=gs, user_table=user_table.id)

        cell = generator(worksheet.findall("Уснул"))
        row = worksheet.find(str(now_date()))._row
        column = worksheet.find("Уснул").col

        while check_is_full(gs=gs, users_table=user_table.id, column=column, row=row):
            column = next(cell)._col

        else:
            upload_cell(gs=gs, users_table=user_table.id, row=row, column=column, data=time_from_user)
            if not check_is_full(gs=gs, users_table=user_table.id, row=row, column=column-1):
                upload_cell(gs=gs, users_table=user_table.id, row=row, column=column-1, data=time_from_user)

            bot.send_message(message.chat.id, f'малыш уснул в {time_from_user}')

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(types.KeyboardButton('Проснулся'))
            bot.send_message(message.chat.id, f'добавить следующее действие', reply_markup=markup)

    elif action_from_user.lower() == 'проснулся':

        create_new_day(gs=gs, user_table=user_table.id)
        cell = generator(worksheet.findall("Проснулся"))
        row = worksheet.find(now_date())._row
        column = worksheet.find("Проснулся").col

        while check_is_full(gs=gs, users_table=user_table.id, column=column, row=row):
            column = next(cell)._col
        else:
            upload_cell(gs=gs, users_table=user_table.id, row=row, column=column, data=time_from_user)
            bot.send_message(message.chat.id, f'малыш проснулся в {time_from_user}')

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(types.KeyboardButton('Уснул'))
            bot.send_message(message.chat.id, f'добавить следующее действие', reply_markup=markup)

    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton('Уснул'))
        bot.send_message(message.chat.id, f'вы написали что-то не то', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def handle_text(message):
    user_table = table(gs=gs, users_table=user_spreadsheetId(message))
    worksheet = user_table.get_worksheet(0)

    if message.text.strip() == 'Уснул':
        create_new_day(gs=gs, user_table=user_table.id)

        cell = generator(worksheet.findall("Уснул"))
        row = worksheet.find(str(now_date()))._row
        column = worksheet.find("Уснул").col

        while check_is_full(gs=gs, users_table=user_table.id, column=column, row=row):
            column = next(cell)._col

        else:
            upload_cell(gs=gs, users_table=user_table.id, row=row, column=column, data=now_time())
            if not check_is_full(gs=gs, users_table=user_table.id, row=row, column=column-1):
                upload_cell(gs=gs, users_table=user_table.id, row=row, column=column-1, data=now_time())

            bot.send_message(message.chat.id, f'малыш уснул в {now_time()}')

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(types.KeyboardButton('Проснулся'))
            bot.send_message(message.chat.id, f'добавить следующее действие', reply_markup=markup)

    elif message.text.strip() == 'Проснулся':
        create_new_day(gs=gs, user_table=user_table.id)

        cell = generator(worksheet.findall("Проснулся"))
        row = worksheet.find(now_date())._row
        column = worksheet.find("Проснулся").col

        while check_is_full(gs=gs, users_table=user_table.id, column=column, row=row):
            column = next(cell)._col
        else:
            upload_cell(gs=gs, users_table=user_table.id, row=row, column=column, data=now_time())
            bot.send_message(message.chat.id, f'малыш проснулся в {now_time()}')

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(types.KeyboardButton('Уснул'))
            bot.send_message(message.chat.id, f'добавить следующее действие', reply_markup=markup)





bot.polling(none_stop=True)


