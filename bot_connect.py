import json
from time import sleep
from requests import get, post, delete
import logging

import config
from send_msg import s_m, s_m_admin
from bots import bot_journalist



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


def game(const):
    global relationships_bot_police
    global relationships_bot_criminalist

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

    # при плохих отношениях, майор не скажет о времени, а только потом напомнит ему
    time_talk_answer = False

    # Первая развязка (1, 2, 3)
    if relationships_bot_police >= 0:
        post_info('bot_police', 1, 'Я рад, что ты снова с нами в строю')
        time_relationships = wait_answer()
        relationships_bot_police += time_relationships
        if time_relationships < 0:
            post_info('bot_police', 2, 'Совсем страх потерял?')
            if wait_answer() < 0:
                relationships_bot_police += -1
                s_m(f'Я сейчас на исходе, поэтому бегом на '
                    f'место преступления. Это {const["point_1"]}\nКонец связи')
                time_talk_answer = True
            else:
                relationships_bot_police += 1
                s_m('Кратко ввожу в курс дела. Рядом произошёл суицид, сходи да проверь там всё')
                post_info('bot_police', 3, f'Чтобы через {const["time_1"]} мин был там, ок?!')
                relationships_bot_police += wait_answer()
        else:
            s_m('У нас неподалеку совершилось самоубийство. Тебе стоит выехать и разобраться.'
                ' Возможно, здесь что-то не чисто. Это серьёзное дело, будь готов ко всему')
            sleep(2)
            s_m(f'Тебе срочно надо выезжать. Место преступления {const["point_1"]}')
            sleep(1)
            s_m(f'Тебе даётся {const["time_1"]} мин, чтобы добраться до точки и просмотреть место происшествия')
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
                f'Вот координаты, сам разберёшься "{const["coor_1"]}"')
        else:
            s_m(f'Значит неподалеку что-то случилось, выдвигайся туда\nУ тебя есть {const["time_1"]} мин. Вот координаты'
                f' "{const["coor_1"]}"')

    # криминалист
    s_m('Слышал, ты снова с нами\nХотел напомнить, чтобы ты не забывал про меня. А то знаю я тебя...\n', config.TOKEN_CRIMINALIST)

    # криминалист (0, 1)
    post_info('bot_criminalist', 0, 'Я буду помогать тебе с уликами. Отправляй мне все улики, которые найдешь.'
                                    ' Они выглядят примерно так “asdfgq” Я тебе отправлю по ним показания.')

    # ждём ответа
    relationships_bot_criminalist += wait_answer()

    if relationships_bot_criminalist == 0:
        post_info('bot_criminalist', 1, 'Всё по старой схеме')
        relationships_bot_criminalist += wait_answer()

    # первые новости, bot__journalist
    bot_journalist.news_1()

    sleep(20)

    # криминалист, Досье
    s_m('Сосвем забыл скинуть тебе досье. Держи', config.TOKEN_CRIMINALIST)

    sleep(60)  # должно быть 60 = 1мин

    # если нагрубил, то о времени сообщается позже. примерно 5 мин от времени которое даётся
    if time_talk_answer:
        s_m('Совсем забыл сказать, что мы ограничены по времени и работать нужно как можно быстрее,'
            ' иначе приедут федералы и будет худо\nУ тебя на все дела осталось 15 мин', config.TOKEN_POLICE)


def main():
    with open('const_game.json', encoding='utf-8') as file:
        data = json.load(file)['Молокова']  # input()
    game(data)


if __name__ == '__main__':
    main()
