import config
import asyncio
from aiogram import Bot

# глобальная переменная
bot = None


async def send_bot(m):
    await bot.send_message(config.ID_PERSON, m)


def s_m(msg, token_id=''):
    global bot

    # если новый TOKEN
    if token_id:
        bot = Bot(token=token_id)

    send = asyncio.get_event_loop()
    send.run_until_complete(send_bot(msg))

