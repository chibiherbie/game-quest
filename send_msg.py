import config
import asyncio
from aiogram import Bot

# глобальная переменная
bot = None
bot_admin = Bot(token=config.TOKEN_POLICE)  # будет оповещать о значимых моментавх в игре


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


# ---- send message for admin ----
async def admin(m):
    await bot_admin.send_message(config.MY_ID, m)


def s_m_admin(msg):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(admin(msg))