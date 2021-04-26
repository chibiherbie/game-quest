import json
from time import sleep
from requests import get, post, delete, put
import logging

import config
from send_msg import s_m, s_m_admin, s_m_photo, s_m_pos
from bots import bot_journalist
import datetime as dt


# Отношения с игроком
relationships_bot_police, relationships_bot_criminalist = 0, 0
suspect = []

logging.basicConfig(level=logging.INFO)


def post_info(bot, num, text, active=True):
    post(f'{config.URL_B}/{bot}', json={
        "isActive": active,
        "num_block": num,
        "text": text})


def get_info(bot):
    return get(f'{config.URL_B}/{bot}').json()


def wait_answer():
    while True:
        data = get_info('bot_connect')

        if data['isActive']:
            post_info('bot_connect', 0, '', False)
            return data['num_block']
        sleep(1)


def timer(duration):  # time  минутах
    time_start = dt.datetime.now()
    time = 0

    while time <= duration * 60:
        time = (dt.datetime.now() - time_start)  # разница во времени
        time = divmod(time.days * 24 * 60 * 60 + time.seconds, 60)  # пеереводим разницу в "мин:сек"
        time = time[0] * 60 + time[1]  # переводим в сек

        if time % 60 == 0:  # оповещение для админа
            s_m_admin('Прошло ' + str(time // 60) + ' мин от ' + str(duration))

        if get_info('bot_connect')['text'] == 'isPosition':
            print('На позиции')
            post_info('bot_connect', 0, '', active=False)
            return ['no late', round((duration * 60 - time) / 60)]

    return ['late', 0]


def game(const):
    global relationships_bot_police
    global relationships_bot_criminalist

    # очищаем остатки прошлой игры
    delete(f'{config.URL_B}/bot_connect')

    sleep(2)

    s_m_admin('ИГРА НАЧАЛАСЬ')  # сообщенпия для админа
    '''
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

    # ----ПЕРВОЕ УБИЙСВО----

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
    s_m_photo(config.PHOTO_1)  # прикрепляем фото

    sleep(60)  # должно быть 60 = 1мин

    # если нагрубил, то о времени сообщается позже. примерно 5 мин от времени которое даётся
    if time_talk_answer:
        s_m('Совсем забыл сказать, что мы ограничены по времени и работать нужно как можно быстрее,'
            ' иначе приедут федералы и будет худо\nУ тебя на все дела осталось 15 мин', config.TOKEN_POLICE)
    '''
    # идёт таймер, где ждём позицию от игрока..
    # если приходит раньше, запускаем уровень
    # если опаздывает, то не ждём и запускаем уровень
    sleep(10)
    s_m_pos('Жду от тебя сообщение, когда прибудешь на место приступление', config.TOKEN_CRIMINALIST)
    game_time = timer(10)  # на 10 минут, 1 левел

    # если опоздал, запускаем таймер поиска
    if game_time[0] == 'late':
        s_m('Ты опаздываешь! Добирайся быстрее, время уже идёт', config.TOKEN_CRIMINALIST)
        s_m_pos('Как придёшь, сообщи мне и запускай приложение для поиска')

        game_time = timer(5)
        if game_time[0] == 'no late':
            put(f'{config.URL_B}/game', json={'time': game_time[1], 'level': 1}).json()
            sleep(game_time[1] * 60)
    else:
        put(f'{config.URL_B}/game', json={'time': 6, 'level': 1}).json()
        sleep(6 * 60)

    sleep(10)

    s_m('Походу всё... Пора уходить', config.TOKEN_POLICE)

    # мини диалог (5)
    post_info('bot_police', 5, 'Есть какие-то предположения у тебя в голове?')
    relationships_bot_police += wait_answer()

    sleep(1)
    s_m('Теперь мы можем опросить свидетелей и друзей, может они нам что-то расскажут?')

    sleep(2)
    s_m('У нас времени не совсем много, так что ты сможешь опросить только пару человек')

    # bot_police, опрос (6)
    for _ in range(2):
        post_info('bot_police', 6, 'Кого опрашиваем?')
        count = wait_answer()  # выбираем кого опрашиваем

        # диалоги с подозреваемыми
        if count == 1:  # диалог - соседка с этажа (0 - 9)
            sleep(4)
            post_info('bot_talks', 0, 'Здравствуйте, я соседка с Этажа')

            if wait_answer() == 0:  # развязка (1, 2, 3, 4)
                post_info('bot_talks', 1, 'Но он к ней часто приходил')
                if wait_answer() == 0:  # развязка (2, 3, 4)
                    post_info('bot_talks', 2, 'Возможно часам к 8.30')
                    if wait_answer() == 0:  # развязка (3, 4)
                        post_info('bot_talks', 3, 'Через какое-то время я услышала крики')
                        wait_answer()
                        post_info('bot_talks', 4, 'Дальше уже не слышала, ушла')
                        wait_answer()
                    else:
                        post_info('bot_talks', 4, 'Нет, в этот момент я ушла...')
                        wait_answer()
                else:
                    post_info('bot_talks', 4, 'Я бы на Вашем месте опросила его и не спускала глаз!')
                    wait_answer()
            # развязка (4, 5, 6, 7, 8, 9)
            else:
                post_info('bot_talks', 5, 'Но я не уверена')
                if wait_answer() == 0:  # развязка (4, 6, 7)
                    post_info('bot_talks', 6, 'Она кричала на кого-то, что не любит его, но я не уверена')
                    if wait_answer() == 0:  # развязка (4, 7)
                        post_info('bot_talks', 7, 'Я с ней мало знакома')
                        if wait_answer() == 0:  # развязка (4)
                            post_info('bot_talks', 4, 'В этот момент я ушла...')
                            wait_answer()
                    else:
                        post_info('bot_talks', 4, 'В этот момент я ушла...')
                        wait_answer()
                else:  # развязка (4, 8, 9)
                    post_info('bot_talks', 8, 'Мне кажется, тогда она сильно ссорилась со своим парнем')
                    if wait_answer() == 0:  # развязка (4, 9)
                        post_info('bot_talks', 9, 'и «мне страшно одной, вдруг он придет.»')
                        if wait_answer() == 0:
                            post_info('bot_talks', 4, 'Я в этот момент ушла')
                            wait_answer()
                        else:
                            post_info('bot_talks', 4, 'На вашем бы месте я бы его только и проверила')
                            wait_answer()
                    else:
                        post_info('bot_talks', 4, 'Не знаю')
                        wait_answer()

        elif count == 2:  # диалог - сосед этажом ниже (10 - 16)
            sleep(3)
            post_info('bot_talks', 10, 'Здравствуйте, я сосед проживающий этажом ниже')  # отдаём через файл команду

            if wait_answer() == 0:  # развязка (11, 12, 13 )
                post_info('bot_talks', 11, 'Она мне никогда не нравилась')  # отдаём через файл команду
                if wait_answer() == 0:  # развязка (12)
                    post_info('bot_talks', 12, 'Однажды видел её накаченной наркотой')
                    wait_answer()
                else:  # развязка (12, 13 )
                    post_info('bot_talks', 13, 'Иногда оры стоят в квартире и подобное')
                    if wait_answer() == 0:
                        post_info('bot_talks', 12, 'Оры стояли на весь этаж!')
                        wait_answer()
                    else:
                        post_info('bot_talks', 12, 'Больше ничего не знаю')
                        wait_answer()
            else:  # развязка (12, 14, 15, 16)
                post_info('bot_talks', 14, 'Стояли сильные оры на всём этаже')
                if wait_answer() == 0:  # развязка (12, 15)
                    post_info('bot_talks', 15, 'Кричала плохие слова кому-то')
                    if wait_answer() == 0:
                        post_info('bot_talks', 12, 'Больше ничего скзаать не могу')
                        wait_answer()
                    else:
                        post_info('bot_talks', 12, 'Однажды она была под наркотой, может быть из-за этого')
                        wait_answer()
                else:  # развязка (12, 16)
                    post_info('bot_talks', 16, 'Точно, точно')
                    if wait_answer() == 0:
                        post_info('bot_talks', 12, 'Но вроде он ушёл от неё часов в 8')
                        wait_answer()
                    else:
                        post_info('bot_talks', 12, 'Это не точно, слух у меня плохой')
                        wait_answer()

        elif count == 3:  # диалог - лучшая подруга (17 - 23)
            sleep(3)
            post_info('bot_talks', 17, 'Доброе утро,  я её лучшая подруга Алина')
            if wait_answer() == 0:  # развязка (18, 19, 20)
                post_info('bot_talks', 18, 'Она изменилась')
                if wait_answer() == 0:
                    post_info('bot_talks', 19, 'С синяками под глазами и сильно похудела. Будто сильно заболела')
                    wait_answer()
                else:  # развязка (19, 20)
                    post_info('bot_talks', 20, 'Не знаю...')
                    if wait_answer() == 0:
                        post_info('bot_talks', 19, 'Но врагов у неё не было')
                        wait_answer()
                    else:
                        post_info('bot_talks', 19, 'Но я спрашивала у неё, что с ней, но она говорила всё окей')
                        wait_answer()

            else:  # развязка (19, 21, 22, 23)
                post_info('bot_talks', 21, 'Но в какой-то момент у неё были прорблемы с парнем')
                if wait_answer() == 0:  # развязка (19, 22)
                    post_info('bot_talks', 22, 'И очень сильно')
                    if wait_answer() == 0:
                        post_info('bot_talks', 19, 'Не знаю')
                        wait_answer()
                    else:
                        post_info('bot_talks', 19, 'Вполне это мог быть и он...')
                        wait_answer()
                else:  # развязка (19, 23)
                    post_info('bot_talks', 23, 'Также говорила, что она кого-то боиться, и он хочет убить её')
                    if wait_answer() == 0:
                        post_info('bot_talks', 19, 'У них всё было хорошо...')
                        wait_answer()
                    else:
                        post_info('bot_talks', 19, 'Она мало с кем контактировала')
                        wait_answer()

        else:  # диалог - Парень (24)
            sleep(4)
            post_info('bot_talks', 24, 'Добрый день, детектив. Я парень Лены, Олег')
            if wait_answer() == 0:
                post_info('bot_talks', 25, 'И мне пришлось растаться с ней')
                if wait_answer() == 0:
                    post_info('bot_talks', 26, 'Но я так и не узнал, что')
                    if wait_answer() == 0:
                        post_info('bot_talks', 27, 'Я устал и ушёл')
                        wait_answer()
                    else:
                        post_info('bot_talks', 27, 'Только это')
                        wait_answer()

                else:
                    post_info('bot_talks', 28, 'Потом сказала, что ей страшно одной, ведь он её убьет')
                    if wait_answer() == 0:
                        post_info('bot_talks', 27, 'Где-то так')
                        wait_answer()
                    else:
                        post_info('bot_talks', 27, 'Поэтому не хотел')
                        wait_answer()

            else:
                post_info('bot_talks', 29, 'Всегда любил её')
                if wait_answer() == 0:
                    post_info('bot_talks', 27, 'Мне это не понравилось')
                    wait_answer()
                else:
                    post_info('bot_talks', 30, 'Говорила мне, что кто-то хочет её убить, хах')
                    if wait_answer() == 0:
                        post_info('bot_talks', 27, 'Поэтому и не поверил')
                        wait_answer()
                    else:
                        post_info('bot_talks', 27, ' У неё не было врагов')
                        wait_answer()

    sleep(3)

    # выбор подзреваемого
    s_m('Мы узнали много нового и перед нами есть пару подозрительных личностей. '
        'Это парень и подруга. Тебе стоит сделать выбор, кого задержать', config.TOKEN_POLICE)
    post_info('bot_police', 7, 'Если сделаешь неправильный выбор, это может сказаться на расследовнии')

    # подсказка при хороших отношениях с криминалистом
    if relationships_bot_criminalist > 0:
        sleep(1)
        s_m('Просмотрев место происшествия ещё раз, мы обнаружили улику.'
            ' Под ногтями есть кожный эпителий неизвестного мужчины..'
            ' Возможно это что-то значит')

    if wait_answer() == 0:
        sleep(3)
        s_m('Парень задержан\nЕго Алиби - "Я пришел к ней в восьмом часу, может, в 7:10. Ушел от нее в 7:40.'
            '  Я не убивал ее, я ее любил, несмотря вообще ни на что!" Вам решать, врёт он или нет, но проверить '
            'мы сможем его только потом')
        suspect.append('Парень')
    else:
        sleep(3)
        s_m('Подруга задержана\nЕё Алиби - "Я виделась с ней вчера вечером, все было хорошо. В 9 утра я была на другом'
            ' конце города, в универе сдавала долги, можете спросить преподавателя по математике" Вам решать,'
            ' врёт она или нет, но сообщить правду мы смоежм только позже')
        suspect.append('Подруга, Алина')

    # ----ВТОРОЕ УБИЙСТВО----

    # сообщения о новом убийстве админу
    s_m_admin('Начинается второе убийство')


def main():
    with open('json/const_game.json', encoding='utf-8') as file:
        data = json.load(file)['Молокова']  # input()

    game(data)


if __name__ == '__main__':
    main()
