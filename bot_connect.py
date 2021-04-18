import config
from time import sleep
from send_msg import s_m, s_m_admin
import logging

from requests import get, post


# Отношения с игроком
relationships_Bot__police, relationships_Bot__criminalist = 0, 0

logging.basicConfig(level=logging.INFO)


def post_info(bot, active, num, text):
    post(f'http://127.0.0.1:5000/api/{bot}', json={
        "isActive": active,
        "num_block": num,
        "text": text})


def get_info(bot):
    return get(f'http://127.0.0.1:5000/api/{bot}').json()


def game():
    s_m_admin('ИГРА НАЧАЛАСЬ')  # сообщенпия для админа

    # ----ВСТУПЛЕНИЕ----

    # Первые сообщения для подготовки игры. Моделируем ситуацию отсутсвия главного героя
    s_m('Чёрт, детектив, ты где пропал?', config.TOKEN_POLICE)  # функция, позволяющая отправлять сообщения по токену
    s_m('Уже неделя прошла... Где ты пропадаешь???')
    s_m('Если не отвечаешь через неделю, то ты уволен!')
    s_m('У тебя осталось 24 часа, и если ты будешь продолжать меня игнорить, '
        'то скоро будешь валаяться в углу и молить о помощи!')

    post_info('bot_police', True, 0, 'Отвечай как можно скорей!')


if __name__ == '__main__':
    game()




