from aiogram import Bot, Dispatcher, executor, types
import asyncio
from random import choice
from requests import get, post
import logging

import config
from bots_info.fortuneteller import fortuneteller_info


bot = Bot(token=config.TOKEN_FORTUNETELLER)
dp = Dispatcher(bot)

# переменная для выбора блока из сюжета
num = 0

logging.basicConfig(level=logging.INFO)


@dp.message_handler(content_types=['text'])
async def said(message: types.Message):
    for i in range(2):
        if message.text == fortuneteller_info[num][i][0]:
            markup_remove = types.ReplyKeyboardRemove()
            await asyncio.sleep(2)
            await bot.send_message(message.chat.id, fortuneteller_info[num][i][1], reply_markup=markup_remove)

            post(f'http://127.0.0.1:5000/api/bot_connect', json={
                "isActive": True,
                "num_block": fortuneteller_info[num][i][2],
                "text": ''})
            return
    await bot.send_message(message.chat.id, choice(fortuneteller_info[-1]))


async def get_start():
    global num

    while True:
        bot_data = get(f'http://127.0.0.1:5000/api/bot_fortuneteller').json()
        if bot_data['isActive']:
            num = bot_data['num_block']

            markup = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)  # создание клавиатуры

            item1 = types.KeyboardButton(fortuneteller_info[num][0][0])
            item2 = types.KeyboardButton(fortuneteller_info[num][1][0])

            markup.add(item1, item2)

            post(f'http://127.0.0.1:5000/api/bot_fortuneteller', json={
                "isActive": False,
                "num_block": num,
                "text": 'text'})

            await bot.send_message(config.ID_PERSON, bot_data['text'], reply_markup=markup)
        await asyncio.sleep(1)


if __name__ == '__main__':
    dp.loop.create_task(get_start())
    executor.start_polling(dp, skip_updates=True)