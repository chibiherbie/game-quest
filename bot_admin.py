import json
import os
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
from requests import get, post, put, delete
import logging

# import config

bot = Bot(token=os.environ.get("ADMIN", 'config.TOKEN_ADMIN'))
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

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


class Data(StatesGroup):
    put_game = State()


@dp.message_handler(commands=['get_bot'])
async def get_bot(message: types.Message):
    await bot.send_message(message.chat.id, 'Названия бота', reply_markup=inline)


@dp.message_handler(commands=['put_game'])
async def put_game(message: types.Message):
    await Data.put_game.set()
    await bot.send_message(message.chat.id, 'Напиши время (мин) и уровень (1-5) в формате "<время> <уровень>"\n'
                                            'пример: "4 1"')


@dp.message_handler(commands=['get_game'])
async def get_game(message: types.Message):
    data = get(f'{config.URL_B}/game').json()
    await bot.send_message(message.chat.id, data)


@dp.message_handler(commands=['del_bot'])
async def del_game(message: types.Message):
    delete(f'{config.URL_B}/bot_connect')
    await bot.send_message(message.chat.id, 'Ок')


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('bot'))
async def callback_get_bot(callback_query: types.CallbackQuery):
    data = get(f'{config.URL_B}/{callback_query.data}').json()
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, data)


@dp.message_handler(state=Data.put_game)
async def process_name(message: types.Message, state: FSMContext):
    text = message.text.split()

    if len(text) == 2 and text[0].isdigit() and text[1].isdigit():
        data = put(f'{config.URL_B}/game', json={'time': text[0], 'level': text[1]}).json()
        await bot.send_message(message.chat.id, data)
    else:
        await bot.send_message(message.chat.id, "ERROR")

    await state.finish()


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/get_bot", description="Get запрос бота"),
        BotCommand(command="/del_bot", description="Очистка всех ботов"),
        BotCommand(command="/get_game", description="Get запрос игры"),
        BotCommand(command="/put_game", description="Запуск игры")
    ]
    await bot.set_my_commands(commands)

if __name__ == '__main__':
    dp.loop.create_task(set_commands(bot))
    executor.start_polling(dp, skip_updates=True)