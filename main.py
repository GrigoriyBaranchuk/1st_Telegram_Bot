from logic_for_json import open_json, add_user_to_db, user_spreadsheetId
import telebot
from logic import now_time, now_date, generator, multi_replase
from logic_for_spreadsheet_API import create_table, upload_cell, check_is_full, table, create_new_day
import re
import gspread
import emoji


bot = telebot.TeleBot('5973958816:AAHFvf3ql5SvVmyq1azrZcTRU5p8JwQtfLE')
# path = 'service_account.json'
path = '/app/.config/gspread'
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
        bot.send_message(message.chat.id,
                         f'привет, {first_name}, меня зовут "Фея Снов". Я - сонный бот Жени'
                         f' здесь ты сможешь быстро и удобно заполнить дневник снов\n\n\n'
                         f'Что я умею: отмечать за тебя в твоём дневнике снов '
                         f'когда малыш Проснулся и когда Уснул.\n\nЕсли ты не забыл(а) меня вести, то'
                         f' сразу после того как вы Уснули или Проснулись -  нажми на '
                         f'"Уснул" или "Проснулся". Если ты хочешь сам(а) внести время '
                         f'просто напиши мне "Уснул 11:05" или "Проснулся 11:05". \n\n'
                         f'Ах да- Я пойму, если у тебя принцеса, а не принц и ты '
                         f'напишешь мне "Уснула" или "Проснулась"))\n\n Чуствуй себя свободно и не беспокойся '
                         f'за разделитель между часами и минутами, !!!НО!!! помни  что формат '
                         f'времени только 24 часовой (Пример: "Проснулась в 01:12" - твоя малышка проснулась '
                         f'в 12 минут второго ночи). Приятного использования!!!\n\n'
                         f'{emoji.emojize(":SOS_button:")} И если что - звони Жене - не стесьняйся)))))',
                         reply_markup=markup)
    else:
        bot.send_message(message.chat.id, f'Привет {first_name} мы уже общались и у вас уже есть дневник снов'
                                          f' просто нажмите уснул малыш или проснулся',
                         reply_markup=markup)


@bot.message_handler(regexp='([Пп]роснул[а-я]{2,3})(\s){0,2}[в]{0,1}(\s){0,2}([0-2][0-9][:;/.\-,][0-5][0-9]){0,1}')
def handle_time(message):
    user_table = table(gs=gs, users_table=user_spreadsheetId(message))
    worksheet = user_table.get_worksheet(0)
    message_from_user = message.text.strip()
    time_from_user = multi_replase(message_from_user.split(' ')[-1])
    pattern = '[0-2][0-9]:[0-5][0-9]'

    if not re.fullmatch(pattern=pattern, string=time_from_user):
        data = now_time()
    else:
        data = time_from_user

    create_new_day(gs=gs, user_table=user_table.id)
    cell = generator(worksheet.findall("Проснулся"))
    row = worksheet.find(now_date())._row
    column = worksheet.find("Проснулся").col

    while check_is_full(gs=gs, users_table=user_table.id, column=column, row=row):
        column = next(cell)._col
    else:
        upload_cell(gs=gs, users_table=user_table.id, row=row, column=column, data=data)

    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(telebot.types.KeyboardButton('Уснул'))
    bot.send_message(message.chat.id, f'малыш Проснулся в {data}\n\nдобавить следующее действие', reply_markup=markup)


@bot.message_handler(regexp='([Уу]снул[а-я]{0,1})(\s){0,2}[в]{0,1}(\s){0,2}([0-2][0-9][:;/.\-,][0-5][0-9]){0,1}')
def handle_time(message):
    user_table = table(gs=gs, users_table=user_spreadsheetId(message))
    worksheet = user_table.get_worksheet(0)
    message_from_user = message.text.strip()
    time_from_user = multi_replase(message_from_user.split(' ')[-1])
    pattern = '[0-2][0-9]:[0-5][0-9]'

    if not re.fullmatch(pattern=pattern, string=time_from_user):
        data = now_time()
    else:
        data = time_from_user

    create_new_day(gs=gs, user_table=user_table.id)
    cell = generator(worksheet.findall("Уснул"))
    row = worksheet.find(now_date())._row
    column = worksheet.find("Уснул").col

    while check_is_full(gs=gs, users_table=user_table.id, column=column, row=row):
        column = next(cell)._col
    else:
        upload_cell(gs=gs, users_table=user_table.id, row=row, column=column, data=data)
        if not check_is_full(gs=gs, users_table=user_table.id, row=row, column=column - 1):
                    upload_cell(gs=gs, users_table=user_table.id, row=row, column=column-1, data=data)

    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(telebot.types.KeyboardButton('Проснулся'))
    bot.send_message(message.chat.id, f'малыш уснул в {data} \n\nдобавить следующее действие', reply_markup=markup)


# bot.polling(none_stop=True)
bot.infinity_polling(timeout=10, long_polling_timeout=5)

