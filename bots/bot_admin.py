import json
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from requests import get, post, put, delete
import logging

import config

bot = Bot(token=config.TOKEN_ADMIN)
dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)

# inline клавиатура
inline_police = InlineKeyboardButton('police', callback_data='bot_police')
inline_anonym = InlineKeyboardButton('anonym', callback_data='bot_anonym')
inline_criminalist = InlineKeyboardButton('criminalist', callback_data='bot_criminalist')
inline_talks = InlineKeyboardButton('talks', callback_data='bot_talks')
inline_fortuneteller = InlineKeyboardButton('fortuneteller', callback_data='bot_fortuneteller')
inline = InlineKeyboardMarkup().add(inline_police, inline_anonym)
inline.add(inline_criminalist, inline_talks)
inline.add(inline_fortuneteller)


@dp.message_handler(commands=['bot'])
async def get_bot(message: types.Message):
    await bot.send_message(message.chat.id, 'Названия бота', reply_markup=inline)


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('bot'))
async def callback_get_bot(callback_query: types.CallbackQuery):
    data = get(f'{config.URL_B}/{callback_query.data}').json()
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, data)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)