import json

from aiogram import Bot, Dispatcher, executor, types
import asyncio
from random import choice
from requests import get, post
import logging

import config
from bots_info.criminalist import criminalist_info

bot = Bot(token=config.TOKEN_CRIMINALIST)
dp = Dispatcher(bot)

# переменная для выбора блока из сюжета
num = 0

logging.basicConfig(level=logging.INFO)


@dp.message_handler(commands=['skip_pos'])
async def process_start_command(message: types.Message):
    await message.reply("* БЫСТРЫЙ ПРОПУСК ЛОКАЦИИ *")

    markup_remove = types.ReplyKeyboardRemove()

    post(f'{config.URL_B}/bot_connect', json={
        "isActive": False,
        "num_block": 0,
        "text": 'isPosition'})

    await bot.send_message(message.chat.id, 'Так держать, можешь начинать исследовать', reply_markup=markup_remove)
    return


@dp.message_handler(content_types=['text'])
async def said(message: types.Message):
    for i in range(4):
        if message.text == criminalist_info[num][i][0]:
            markup_remove = types.ReplyKeyboardRemove()
            await asyncio.sleep(2)
            await bot.send_message(message.chat.id, criminalist_info[num][i][1], reply_markup=markup_remove)

            post(f'{config.URL_B}/bot_connect', json={
                "isActive": True,
                "num_block": criminalist_info[num][i][2],
                "text": ''})
            return
    # await bot.send_message(message.chat.id, choice(criminalist_info[-1]))


@dp.message_handler(content_types=['location'])
async def location(message: types.location):
    with open('../json/const_game.json', encoding='utf-8') as file:
        data = json.load(file)

    # если игрок на назначеном месте, то даём возможность искать улики
    for coor in data['Молокова']['square_coor']:
        if coor[0] < message.location.latitude < coor[1] and coor[2] < message.location.longitude < coor[3]:
            # print('На месте')

            markup_remove = types.ReplyKeyboardRemove()

            post(f'{config.URL_B}/bot_connect', json={
                "isActive": False,
                "num_block": 0,
                "text": 'isPosition'})

            await bot.send_message(message.chat.id, 'Так держать, можешь начинать исследовать', reply_markup=markup_remove)
            return
    # print(message.location)
    await bot.send_message(message.chat.id, 'Ты ещё не на месте, давай поторопись')


async def get_start():
    global num

    while True:
        bot_data = get(f'{config.URL_B}/bot_criminalist').json()
        if bot_data['isActive']:
            num = bot_data['num_block']

            markup = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)  # создание клавиатуры

            item1 = types.KeyboardButton(criminalist_info[num][0][0])
            item2 = types.KeyboardButton(criminalist_info[num][1][0])
            item3 = types.KeyboardButton(criminalist_info[num][2][0])
            item4 = types.KeyboardButton(criminalist_info[num][3][0])

            markup.add(item1, item2, item3, item4)

            post(f'{config.URL_B}/bot_criminalist', json={
                "isActive": False,
                "num_block": num,
                "text": 'text'})

            await bot.send_message(config.ID_PERSON, bot_data['text'], reply_markup=markup)
        await asyncio.sleep(1)


if __name__ == '__main__':
    dp.loop.create_task(get_start())
    executor.start_polling(dp, skip_updates=True)