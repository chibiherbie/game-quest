import config
from time import sleep
from send_msg import s_m
import logging


# Отношения с игроком
relationships_Bot__police, relationships_Bot__criminalist = 0, 0

logging.basicConfig(level=logging.INFO)

# ----ВСТУПЛЕНИЕ----

# Первые сообщения для подготовки игры. Моделируем ситуацию отсутсвия главного героя
s_m('Чёрт, Паша, ты где пропал?', config.TOKEN_POLICE)  # функция, позволяющая отправлять сообщения по токену
s_m('Уже неделя прошла... Где ты пропадаешь???')
s_m('Если не отвечаешь через неделю, то ты уволен!')
s_m('У тебя осталось 24 часа, и если ты будешь продолжать меня игнорить, '
    'то скоро будешь валаяться в углу и молить о помощи!')



