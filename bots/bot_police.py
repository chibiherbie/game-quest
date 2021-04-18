import logging
import config
from aiogram import Bot, Dispatcher, executor, types
import asyncio
from bots_info.police import police_info
from random import choice


bot = Bot(token=config.TOKEN_POLICE)
dp = Dispatcher(bot)

# переменная для выбора блока из сюжета
num = 0
relationships = 0

logging.basicConfig(level=logging.INFO)


@dp.message_handler(content_types=['text'])
async def said(message: types.Message):
    for i in range(4):
        if message.text == police_info[num][i][0]:
            markup_remove = types.ReplyKeyboardRemove()
            await asyncio.sleep(2)
            await bot.send_message(message.chat.id, police_info[num][i][1], reply_markup=markup_remove)
            break
    await bot.send_message(message.chat.id, choice(police_info[-1]))


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)