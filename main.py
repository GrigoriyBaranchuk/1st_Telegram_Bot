from logic_for_json import open_json, add_user_to_db, user_spreadsheetId
import telebot
from logic import now_time, now_date, generator, multi_replase
from logic_for_spreadsheet_API import create_table, upload_cell, check_is_full, table, create_new_day
import re
import gspread
import emoji
import time
from texts import hello_text, you_have_table




bot = telebot.TeleBot('5973958816:AAHFvf3ql5SvVmyq1azrZcTRU5p8JwQtfLE')
path = 'service_account.json'
# path = '/app/.config/gspread'
gs = gspread.service_account(filename=path)


@bot.message_handler(commands=['start'])
def start(message):
    """
    message.chat.id - chat identifier
    message.from_user.first_name - first name of user.
    We are able to take any information about user from message.from_user]
    """
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(telebot.types.KeyboardButton('Уснул'))
    markup.add(telebot.types.KeyboardButton('Проснулся'))

    first_name = message.from_user.first_name
    user_id = str(message.from_user.id)
    users_list = [inst['pk'] for inst in open_json()] #crate list of users pk from db
    if user_id not in users_list:
        spreadsheetId = create_table(gs=gs, name=first_name)
        to_json = {"pk": user_id, "first_name": first_name, "spreadsheetId": spreadsheetId}
        add_user_to_db(to_json)
        bot.send_message(message.chat.id, hello_text.format(name=first_name, book=emoji.emojize(":open_book:"),
                                                            face=emoji.emojize(":sleeping_face:"),
                                                            boy=emoji.emojize(":baby:"),
                                                            girl=emoji.emojize(":girl:"),
                                                            exclamation=emoji.emojize(":red_exclamation_mark:"),
                                                            sos=emoji.emojize(":SOS_button:")
                                                            ),
                         reply_markup=markup)
    else:
        bot.send_message(message.chat.id, you_have_table.format(name=first_name, book=emoji.emojize(":open_book:")),
                         reply_markup=markup)


@bot.message_handler(regexp='([Пп]роснул[а-я]{2,3})(\s){0,2}[в]{0,1}(\s){0,2}([0-2][0-9][:;/.\-,][0-5][0-9]){0,1}')
def handle_time(message):

    user_table = table(gs=gs, users_table=user_spreadsheetId(message))
    worksheet = user_table.get_worksheet(0)
    message_from_user = message.text.strip()
    time_from_user = multi_replase(message_from_user.split(' ')[-1])
    pattern = '[0-2]{0,1}[0-9]:[0-5][0-9]'

    if not re.fullmatch(pattern=pattern, string=time_from_user):
        data = now_time()
    else:
        data = time_from_user

    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(telebot.types.KeyboardButton('Уснул'))
    bot.send_message(message.chat.id, f'малыш Проснулся в {data}\n\nдобавить следующее действие', reply_markup=markup)

    create_new_day(gs=gs, user_table=user_table.id)
    cell = generator(worksheet.findall("Проснулся"))
    row = worksheet.find(now_date())._row
    column = worksheet.find("Проснулся").col

    while check_is_full(gs=gs, users_table=user_table.id, column=column, row=row):
        column = next(cell)._col
        time.sleep(0.5)
    else:
        upload_cell(gs=gs, users_table=user_table.id, row=row, column=column, data=data)




@bot.message_handler(regexp='([Уу]снул[а-я]{0,1})(\s){0,2}[в]{0,1}(\s){0,2}([0-2][0-9][:;/.\-,][0-5][0-9]){0,1}')
def handle_time(message):
    user_table = table(gs=gs, users_table=user_spreadsheetId(message))
    worksheet = user_table.get_worksheet(0)
    message_from_user = message.text.strip()
    time_from_user = multi_replase(message_from_user.split(' ')[-1])
    pattern = '[0-2]{0,1}[0-9]:[0-5][0-9]'

    if not re.fullmatch(pattern=pattern, string=time_from_user):
        data = now_time()
    else:
        data = time_from_user

    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(telebot.types.KeyboardButton('Проснулся'))
    bot.send_message(message.chat.id, f'малыш уснул в {data} \n\nдобавить следующее действие', reply_markup=markup)

    create_new_day(gs=gs, user_table=user_table.id)
    cell = generator(worksheet.findall("Уснул"))
    row = worksheet.find(now_date())._row
    column = worksheet.find("Уснул").col

    while check_is_full(gs=gs, users_table=user_table.id, column=column, row=row):
        column = next(cell)._col
        time.sleep(0.5)
    else:
        upload_cell(gs=gs, users_table=user_table.id, row=row, column=column, data=data)
        if not check_is_full(gs=gs, users_table=user_table.id, row=row, column=column - 1):
                    upload_cell(gs=gs, users_table=user_table.id, row=row, column=column-1, data=data)


# bot.polling(none_stop=True)
bot.infinity_polling(timeout=10, long_polling_timeout=5)

