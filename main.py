from aiogram import Bot, Dispatcher, types, executor
import config
import sqlite3
import datetime
from aiogram.types.web_app_info import WebAppInfo

bot = Bot(config.BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    data={
        "NAME": message.from_user.first_name,
        "SURNAME": message.from_user.last_name,
        "IS_SUBCRIBED": False,
        "CHAT_ID": message.chat.id,
        "SLEEP_TIME": '00:00',
        "WAKE_UP_TIME" :'00:00'
    }
    while True:
        await bot.send_message(1389092057,'хуй')

    con = sqlite3.connect('sleppy.sql')
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS users (id INTEGER AUTO INCREMENT PRIMARY KEY, chat_id INTEGER NOT NULL UNIQUE , name varchar(250) NOT NULL, surname varchar(250) NOT NULL,wake_up varchar(250) NOT NULL,sleep_time varchar(250) NOT NULL,is_subcribed BOOLEAN)""")
    try:
        cur.execute("""INSERT INTO users (chat_id, name, surname,wake_up,sleep_time,is_subcribed) VALUES ('%s','%s','%s','%s','%s','%s')""" % (data['CHAT_ID'],data['NAME'],data['SURNAME'],data['WAKE_UP_TIME'],data['SLEEP_TIME'],data['IS_SUBCRIBED']))
    except:
        await bot.send_message(message.chat.id, 'Если хочешь начать заново напиши в нашу поддержку')
    cur.execute("""SELECT * FROM users""")
    await bot.send_message(message.chat.id,cur.fetchall())
    con.commit()
    cur.close()
    con.close()

    markup = types.InlineKeyboardMarkup(one_time_keyboard=True)
    btn1 = types.InlineKeyboardButton("Начать курс 💪", callback_data="start")
    markup.add(btn1)
    await bot.send_message(message.chat.id,f' Привет !\n\nКажется, мы с тобой ещё не прошли подготовку к курсу. Давай начнём?',reply_markup=markup)

@dp.callback_query_handler()
async def callback_query(call):
    if call.data =="start":
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton("Спасибо тебе", callback_data="first")
        btn2= types.InlineKeyboardButton("Я хочу полную версию", callback_data="full")
        markup.add(btn1,btn2)
        await call.message.edit_text(f'Привет !\n\nКажется, мы с тобой ещё не прошли подготовку к курсу. Давай начнём?\n\n Начать курс 💪')
        await bot.send_message(call.message.chat.id, 'Отлично,я вижу мы с тобой подружимся\n\nДам тебе 3 дня,что-бы оценить наш курс',reply_markup=markup)

executor.start_polling(dp)