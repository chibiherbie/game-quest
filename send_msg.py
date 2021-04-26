import config
import asyncio
from aiogram import Bot, types


# глобальная переменная
bot = Bot(token=config.TOKEN_POLICE)
bot_admin = Bot(token=config.TOKEN_ADMIN)  # будет оповещать о значимых моментавх в игре


# ---- send message for bots ----
async def send_bot(m):
    await bot.send_message(config.ID_PERSON, m)


def s_m(msg, token_id=''):
    global bot

    # если новый TOKEN
    if token_id:
        bot = Bot(token=token_id)

    send = asyncio.get_event_loop()
    send.run_until_complete(send_bot(msg))


# ---- send pos for bot ----
async def send_bot_pos(m, btn):
    await bot.send_message(config.ID_PERSON, m, reply_markup=btn)


def s_m_pos(msg, token_id=''):
    global bot

    # если новый TOKEN
    if token_id:
        bot = Bot(token=token_id)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  # создание клавиатуры
    markup.add(types.KeyboardButton('Отправить свою гео', request_location=True))

    send = asyncio.get_event_loop()
    send.run_until_complete(send_bot_pos(msg, markup))


# ---- send message for admin ----
async def admin(m):
    await bot_admin.send_message(config.MY_ID, m)


def s_m_admin(msg):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(admin(msg))


# ---- send photo ----

async def photo(m):
    await bot.send_photo(config.ID_PERSON, m)


# для отправки фото
def s_m_photo(msg, token_id=''):
    global bot

    # если новый TOKEN
    if token_id:
        bot = Bot(token=token_id)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(photo(msg))