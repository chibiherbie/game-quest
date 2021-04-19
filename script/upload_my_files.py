import os
import asyncio
from aiogram import Bot
from config import TOKEN_POLICE, MY_ID


bot = Bot(token=TOKEN_POLICE)

BASE_PATH = '../static/img_game'


async def MediaFiles(method, file_attr):
    folder_path = os.path.join(BASE_PATH)
    for filename in os.listdir(folder_path):
        with open(os.path.join(folder_path, filename), 'rb') as file:
            msg = await method(MY_ID, file)
            if file_attr == 'photo':
                file_id = msg.photo[-1].file_id
            else:
                file_id = getattr(msg, file_attr).file_id
            print(filename + ':  ' + file_id)


loop = asyncio.get_event_loop()

tasks = [
    loop.create_task(MediaFiles(bot.send_photo, 'photo')),
]

wait_tasks = asyncio.wait(tasks)

loop.run_until_complete(wait_tasks)
loop.close()