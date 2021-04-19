import config
from time import sleep
from send_msg import s_m, s_m_admin
import logging

from requests import get, post, delete


# Отношения с игроком
relationships_bot_police, relationships_bot_criminalist = 0, 0

logging.basicConfig(level=logging.INFO)


def post_info(bot, num, text, active=True):
    post(f'http://127.0.0.1:5000/api/{bot}', json={
        "isActive": active,
        "num_block": num,
        "text": text})


def get_info(bot):
    return get(f'http://127.0.0.1:5000/api/{bot}').json()


def wait_answer():
    while True:
        data = get_info('bot_connect')
        if data['isActive']:
            post_info('bot_connect', 0, '', False)
            return data['num_block']
        sleep(1)


def game():
    global relationships_bot_police

    # очищаем остатки прошлой игры
    delete('http://127.0.0.1:5000/api/bot_connect')

    s_m_admin('ИГРА НАЧАЛАСЬ')  # сообщенпия для админа

    # ----ВСТУПЛЕНИЕ----

    # Первые сообщения для подготовки игры. Моделируем ситуацию отсутсвия главного героя
    s_m('Чёрт, детектив, ты где пропал?', config.TOKEN_POLICE)  # функция, позволяющая отправлять сообщения по токену
    s_m('Уже неделя прошла... Где ты пропадаешь???')
    s_m('Если не отвечаешь через неделю, то ты уволен!')
    s_m('У тебя осталось 24 часа, и если ты будешь продолжать меня игнорить, '
        'то скоро будешь валаяться в углу и молить о помощи!')

    post_info('bot_police', 0, 'Отвечай как можно скорей!')

    relationships_bot_police += wait_answer()

    # Первая развязка (1, 2, 3)
    if relationships_bot_police >= 0:
        post_info('bot_police', 1, 'Я рад, что ты снова с нами в строю')
        time_relationships = wait_answer()
        relationships_bot_police += time_relationships
        if time_relationships < 0:
            post_info('bot_police', 2, 'Совсем страх потерял?')
            if wait_answer() < 0:
                relationships_bot_police += -1
                s_m('Я сейчас на исходе, поэтому бегом на '
                       'место преступления в парк имени 400-летия на десткую площадку"\nКонец связи')
                time_talk_answer = True
            else:
                relationships_bot_police += 1
                s_m('Кратко ввожу в курс дела. Рядом произошёл суицид, сходи да проверь там всё')
                post_info('bot_police', 3, 'Чтобы через 15 мин был там, ок?!')
                relationships_bot_police += wait_answer()
        else:
            s_m('У нас неподалеку совершилось самоубийство. Тебе стоит выехать и разобраться.'
                ' Возможно, здесь что-то не чисто. Это серьёзное дело, будь готов ко всему')
            sleep(2)
            s_m('Тебе срочно надо выезжать в парк имени 400-летия на десткую площадку, ведь всё возможно')
            sleep(1)
            s_m('Тебе даётся 15 мин, чтобы добраться до точки и просмотреть место происшествия')
            sleep(1)
            post_info('bot_police', 3, 'Всё уяснил, детектив?')
            relationships_bot_police += wait_answer()

    # Вторая развязка (4)
    else:
        post_info('bot_police', 4, 'Лучше бы заткнулся и послушал меня, пока не стало хуже!')
        time_relationships = wait_answer()
        relationships_bot_police += time_relationships
        if time_relationships < 0:
            time_talk_answer = True
            s_m('Я сейчас на пределе, и если ты хочешь обсудить это, то лучше перенести это\n'
                   'А сейчас выдвигайся на место происшествие и как можно скорее. '
                   'Вот координаты, сам разберёшься "56.040239, 92.920635"')
        else:
            s_m('Значит неподалеку что-то случилось, выдвигайся туда\nУ тебя есть 20 мин. Вот координаты'
                   ' "56.040239, 92.920635"')


if __name__ == '__main__':
    game()

