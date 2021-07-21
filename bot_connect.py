from time import sleep
import datetime as dt
from requests import get, post, delete, put
import logging
import json

import config
from send_msg import s_m, s_m_admin, s_m_photo, s_m_pos
from bots import bot_journalist


# Отношения с игроком
relationships_bot_police, relationships_bot_criminalist = 0, 0
# подозреваемые со всей игры
suspect = []

PHOTO_1 = 'AgACAgIAAxkDAAIBcV8QPvYaD3u0_ZPyt8w3VdCwOqX1AAJkrjEbPNiBSCta4itSNvIxZJvfky4AAwEAAwIAA20AA2bKAgABGgQ'
PHOTO_2 = 'AgACAgIAAxkDAAIBcl8QPvfIUXWjneqA4r78pJjMLBdBAAJlrjEbPNiBSDGYrVxwYlWZ5k71lC4AAwEAAwIAA3kAA-T_AQABGgQ'
PHOTO_3 = 'AgACAgIAAxkDAAIBc18QPvf3QXgY7CHgfaCLfWvzvXfgAAJmrjEbPNiBSIrzaHZbLVRcLP7ski4AAwEAAwIAA3kAAzHXAwABGgQ'
PHOTO_4 = 'AgACAgIAAxkDAAIBsV8QTNpMgQgJVhLl2hTFU_7lYbKJAAJ-rjEbPNiBSJFGvLUqu6ZgyQABUZEuAAMBAAMCAAN5AANn9gUAARoE'
PHOTO_5 = 'AgACAgIAAxkDAAIBdF8QPvjbnwmpwXUxXmL3AUIlE8YpAAJnrjEbPNiBSC4S9kk5zc1Ka_zski4AAwEAAwIAA3kAA2rSAwABGgQ'
PHOTO_6 = 'AgACAgIAAxkDAAIBdV8QPvlyIi-B0on72v1mbaq2UtH2AAJorjEbPNiBSCHUwW0WJPT2dvHpki4AAwEAAwIAA3kAA_jWAwABGgQ'
DOWNLOAD_FILE = 'https://disk.yandex.ru/d/ZMN-4v_1nPYxNw'

# логирование
logging.basicConfig(level=logging.INFO)


# посылаем на сервер информацию бота
def post_info(bot, num, text, active=True):
    post(f'{config.URL_B}/{bot}', json={
        "isActive": active,
        "num_block": num,
        "text": text})


# информация бота с сервера
def get_info(bot):
    return get(f'{config.URL_B}/{bot}').json()


# делаем запрос на сервер и ждём результат от боа
def wait_answer():
    while True:
        data = get_info('bot_connect')

        if data['isActive']:
            post_info('bot_connect', 0, '', False)
            return data['num_block']
        sleep(1)


# таймер для ожидания игрока на позиции
def timer(duration):  # time  минутах
    time_start = dt.datetime.now()
    time = 0

    while time <= duration * 60:
        time = (dt.datetime.now() - time_start)  # разница во времени
        time = divmod(time.days * 24 * 60 * 60 + time.seconds, 60)  # пеереводим разницу в "мин:сек"
        time = time[0] * 60 + time[1]  # переводим в сек

        if time % 60 == 0:  # оповещение для админа
            s_m_admin('Время: ' + str(time // 60) + ' мин от ' + str(duration))
            sleep(1)

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

    s_m_admin('Игра началась')  # сообщенпия для админа
    
    # ----ВСТУПЛЕНИЕ----

    # Первые сообщения для подготовки игры. Моделируем ситуацию отсутсвия главного героя
    s_m('Чёрт, детектив, ты где пропал?', config.TOKEN_POLICE)  # функция, позволяющая отправлять сообщения по токену
    s_m('Уже неделя прошла... Где ты пропадаешь???')
    s_m('Если не отвечаешь через неделю, то ты уволен!')
    s_m('У тебя осталось 24 часа, и если ты будешь продолжать меня игнорить, '
        'то скоро будешь валаяться в углу и молить о помощи!')

    post_info('bot_police', 0, 'Отвечай как можно скорей!')  # делаем post запрос на сервер для бота

    relationships_bot_police += wait_answer()  # ожидаем результат и прибавляем к отношениям с персонажем

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
    s_m('Слышал, ты снова с нами\nХотел напомнить, чтобы ты не забывал про меня. А то знаю я тебя...\n',
        config.TOKEN_CRIMINALIST)

    # криминалист (0, 1)
    post_info('bot_criminalist', 0, 'Я буду помогать тебе в процессе расследования и с уликами.')

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
    s_m_photo(PHOTO_1)  # прикрепляем фото
    # s_m('И также, пока не забыл. У тебя есть личный кабинет, с помощью которого ты можешь искать улики. '
    #     'Думаю сам разберёшься')
    # s_m(f'Вот твой id - {get_info("game")["user_id"]}.\nСсылка для скачивания - {DOWNLOAD_FILE}')

    sleep(60)  # должно быть 60 = 1мин

    # если нагрубил, то о времени сообщается позже. примерно 5 мин от времени которое даётся
    if time_talk_answer:
        s_m('Совсем забыл сказать, что мы ограничены по времени и работать нужно как можно быстрее,'
            f' иначе приедут федералы и будет худо\n'
            f'У тебя на все дела осталось примерно {const["time_1"]} мин', config.TOKEN_POLICE)

    # идёт таймер, где ждём позицию от игрока..
    # если приходит раньше, запускаем уровень
    # если опаздывает, то не ждём и запускаем уровень
    sleep(10)
    s_m_pos('Жду от тебя сообщение, когда прибудешь на место приступление', config.TOKEN_CRIMINALIST)
    game_time = timer(int(const['time_1']) - 3)  # на 12 минут, 1 левел

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
        sleep(2)
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

    sleep(10)
    s_m('Так, сейчас нам сообщили о новом происшествие')
    sleep(3)
    s_m('Убит мужчина, 40 лет. Тело найдено в загородном доме района Алексеева предположительно'
        ' причина смерти: самоубийство, '
        'застрелился, пуля прошла навылет с правой стороны висков')
    sleep(1)
    post_info(f'bot_police', 8, f'Время смерти: {dt.date.today().strftime("%d.%m.%Y")},'
                                f' {(dt.datetime.now() - dt.timedelta(minutes=5)).strftime("%H:%M")}')

    time_relationships = wait_answer()
    relationships_bot_police += time_relationships

    if time_relationships == -1:
        post_info('bot_police', 9, 'Второе убийство не может быть хорошим...')
        relationships_bot_police += wait_answer()

    sleep(300)  # перед отправкой досье, 300cек = 5мин
    s_m('Досье готово, Держи', config.TOKEN_CRIMINALIST)
    s_m_photo(PHOTO_2)

    sleep(120)  # перед отправкой новостей, 120сек = 2 мин

    # Вторые новости, bot__journalist
    bot_journalist.news_2()

    # идёт таймер, где ждём позицию от игрока..
    # если приходит раньше, запускаем уровень
    # если опаздывает, то не ждём и запускаем уровень
    sleep(10)
    s_m_pos('Жду от тебя сообщение, когда прибудешь на место приступление', config.TOKEN_CRIMINALIST)
    game_time = timer(int(const['time_2']) - 7)  # на 8 минут, 2 левел

    # если опоздал, запускаем таймер поиска
    if game_time[0] == 'late':
        s_m('Время на исходе... Добирайся быстрее, время уже идёт', config.TOKEN_CRIMINALIST)
        s_m_pos('Как придёшь, сообщи мне и запускай приложение для поиска!')

        game_time = timer(5)
        if game_time[0] == 'no late':
            put(f'{config.URL_B}/game', json={'time': game_time[1], 'level': 2}).json()
            sleep(game_time[1] * 60)
    else:
        put(f'{config.URL_B}/game', json={'time': 6, 'level': 2}).json()
        sleep(6 * 60)

    sleep(10)

    # переход к подозреваемым
    s_m('К нам уже приближаются, пора уходить', config.TOKEN_POLICE)
    sleep(5)
    s_m('Теперь пришло время опросить свидетелей и знакомых. Времени у нас также немного,'
        ' поэтому давай быстрее, кого успеешь опросить')

    # разговор с подозреваемыми
    for _ in range(2):
        post_info('bot_police', 10, 'Выбирай, кого вызвать')
        count = wait_answer()  # выбираем кого опрашиваем

        # диалоги с подозреваемыми
        if count == 1:  # диалог - соседка загородного дома (31 - 35)
            post_info('bot_talks', 31, 'Добрый день, я соседка живущая напротив')
            if wait_answer() == 0:  # (32, 33, 34)
                post_info('bot_talks', 32, 'Вроде чтобы побыть одному')
                if wait_answer() == 0:
                    post_info('bot_talks', 33, 'это было странно')
                    if wait_answer() == 0:
                        post_info('bot_talks', 34, 'Мы с ним мало общаемся')
                        wait_answer()
                    else:
                        post_info('bot_talks', 34, 'всё было тихо')
                        wait_answer()
                else:
                    post_info('bot_talks', 34, 'Больше ничего такого')
                    wait_answer()
            else:  # (34, 35)
                post_info('bot_talks', 35, 'Решили постучаться, но квартира была открыта. Зашли, а там он')
                if wait_answer() == 0:
                    post_info('bot_talks', 34, 'Мы с ним мало общаемся')
                    wait_answer()
                else:
                    post_info('bot_talks', 34,
                              ' Только вот, что он приезжал один раз в два месяца, чтобы побыть одному')
                    wait_answer()

        elif count == 2:  # диалог - Жена (36 - 40)
            post_info('bot_talks', 36, 'Здравствуйте. Я Алёна, жена Арсения')
            if wait_answer() == 0:
                post_info('bot_talks', 37, 'Я не могу сказать, кто это мог сделать')
                if wait_answer() == 0:
                    post_info('bot_talks', 38, 'Обычно он этого не делает')
                    if wait_answer() == 0:
                        post_info('bot_talks', 39, 'По типу «это все он...», а кто-он, я не знаю...')
                        wait_answer()
                    else:
                        post_info('bot_talks', 39, 'Зачем ему это?')
                        wait_answer()
                else:
                    post_info('bot_talks', 39, 'Это было странно, он никогда себя так вел.')
                    wait_answer()
            else:
                post_info('bot_talks', 40, 'Ужас...')
                if wait_answer() == 0:
                    post_info('bot_talks', 39, 'Может, совсем с ума сошла?')
                    wait_answer()
                else:
                    post_info('bot_talks', 39, 'Не думаю что именно сечас он решил сделать это')
                    wait_answer()

        else:  # диалог - Хозяйка мертвой собаки, жертва неудачной операции (41 - 45)
            post_info('bot_talks', 41, 'Привет. Я хозяйка той самой мертвой собаки')
            if wait_answer() == 0:
                post_info('bot_talks', 42, 'Да..Точно')
                if wait_answer() == 0:
                    post_info('bot_talks', 45, 'И только')
                    wait_answer()
                else:
                    post_info('bot_talks', 45, 'Но я не буду опускаться до убийства')
                    wait_answer()

            else:
                post_info('bot_talks', 43, 'Не общаюсь')
                if wait_answer() == 0:
                    post_info('bot_talks', 45, 'Но я не буду опускаться до убийства')
                    wait_answer()
                else:
                    post_info('bot_talks', 44, 'Но если возврощаться к моей собаке, то до меня дошли слухи,'
                                               ' что он был под кайфом во время операции')
                    if wait_answer() == 0:
                        post_info('bot_talks', 45, 'т.к. это была большая ошибка')
                        wait_answer()
                    else:
                        post_info('bot_talks', 45, 'Верить ли...')
                        wait_answer()

    sleep(3)

    # выбор подозреваемого
    s_m('Я думаю тут есть  пара подозритекльных личностей.  Жена и Хозяйка собаки')
    post_info('bot_police', 11, 'Что думаешь, кто из них?')

    if wait_answer() == 0:
        s_m('Хм... Хорошо\nЕё алиби:  В это время я была на кладбище, мне было тяжело, я волновалась, поэтому'
            ' пошла на могилу матери. Я всегда там бываю, когда мне плохо. И вообще, как вы смеете меня подозревать?'
            ' Я любила его, а вовсе не желала ему смерти!»')

    else:
        s_m('Я тоже так считаю\nЕё алиби: Я была на приёме у стоматолога, с 10:40 до 11:50 включительно.»')

        sleep(4)
        # диалог с криминалистом, если отношения >= -1 (2 - 8)
        if relationships_bot_criminalist >= -1:
            post_info('bot_criminalist', 2, 'Почему ты решил выбрать её?')
            time_relationships = wait_answer()
            relationships_bot_criminalist += time_relationships

            if time_relationships == 0:  # (3, 4, 5, 6)
                post_info('bot_criminalist', 3, 'Чем именно?')
                time_relationships = wait_answer()

                if time_relationships == 1:
                    post_info('bot_criminalist', 4, 'Хочу узнать, почему ты выбрал её')
                    time_relationships = wait_answer()

                    if time_relationships == 1:
                        post_info('bot_criminalist', 5, 'Мне показалось, что такая женщина и не может врать. Она знает'
                                                        ', что дело серьёзное и как-бы она не было зла на него, она не '
                                                        'врала бы')
                        time_relationships = wait_answer()
                        relationships_bot_criminalist += time_relationships

                        if time_relationships == 0:
                            post_info('bot_criminalist', 6,
                                      'Но она наговорила за чем-то на эту женщину. Возможно из-за'
                                      ' страха, но выглядело это как отвод подозрения')
                            relationships_bot_criminalist += wait_answer()

                    elif time_relationships == 2:
                        post_info('bot_criminalist', 5,
                                  'Нам важны любые данные. Не думаю, что она это сделала для себя, '
                                  'а не для нас. Как по мне, жена более подозрительный')
                        time_relationships = wait_answer()
                        relationships_bot_criminalist += time_relationships

                        if time_relationships == 0:
                            post_info('bot_criminalist', 6,
                                      'Но она наговорила за чем-то на эту женщину. Возможно из-за'
                                      ' страха, но выглядело это как отвод подозрения')
                            relationships_bot_criminalist += wait_answer()

                    elif time_relationships == 3:
                        post_info('bot_criminalist', 6, 'На твоём бы месте я поменял подозреваемого')
                        relationships_bot_criminalist += wait_answer()

                    else:
                        s_m('Я бы на твоём месте поменял мнение', config.TOKEN_CRIMINALIST)

                elif time_relationships == 2:
                    s_m('Мне показалось, что такая женщина и не может врать. Она знает, что дело серьёзное и как-бы'
                        ' она не было зла на него, она не врала бы', config.TOKEN_CRIMINALIST)

                elif time_relationships == 3:
                    s_m('Нам важны любые данные. Не думаю, что она это сделала для себя, а не для нас',
                        config.TOKEN_CRIMINALIST)

                else:
                    relationships_bot_criminalist += -1
                    s_m('Я хотел только помочь... Мне кажется это не она и всё... Ладно')
            elif time_relationships == 1:  # (7, 8)
                post_info('bot_criminalist', 7, 'Только интуиция?')
                time_relationships = wait_answer()
                relationships_bot_criminalist += time_relationships

                if time_relationships == 1:
                    post_info('bot_criminalist', 8, 'Я конечно не эксперт и тд, но подумай ещё раз')
                    time_relationships += wait_answer()

        sleep(20)

        # мини диалог (12, 13, 14)
        post_info('bot_police', 12, 'Мне тут сообщили, что ты сомвневался в своём выборе. Желаешь его поменять?')
        time_relationships = wait_answer()

        relationships_bot_criminalist += time_relationships
        if time_relationships == 0:
            post_info('bot_police', 13, '???')
            time_relationships = wait_answer()

            if time_relationships == 1:
                post_info('bot_police', 14, 'Но выбор за тобой')
                time_relationships = wait_answer()

                if time_relationships == -1:
                    suspect.append("Жена")
                    relationships_bot_police += time_relationships
                else:
                    suspect.append('Хозяйка собаки')
                    relationships_bot_police += time_relationships

            elif time_relationships == 2:
                suspect.append('Жена')

            else:
                suspect.append('Хозяйка собаки')
        else:
            suspect.append('Хозяйка собаки')

    # ----ТРЕТЬЕ УБИЙСТВО----

    # сообщения о новом убийстве
    s_m_admin('Началось третье убийство')

    sleep(7)
    s_m('Сообщаю о новом убийстве', config.TOKEN_POLICE)
    sleep(5)
    s_m('Убита женщина 39 лет, тело найдено возле дома, в районе Батурина Предположительная причина смерти:'
        ' случайно выпала из окна во время мойки окна. Перелом 80% костей, травмы, несовместимые с жизнью.')
    sleep(2)
    s_m(f'Время смерти: {dt.date.today().strftime("%d.%m.%Y")},'
        f' {(dt.datetime.now() - dt.timedelta(minutes=2)).strftime("%H:%M")}')
    sleep(4)
    s_m(f'Без вяских разговоров выдвигайся по адресу улица {const["point_3"]}.'
        f' У нас не так много времени, всего {const["time_3"]} мин')

    sleep(180)  # 3мин = 180сек
    s_m('Готово, я сделал для тебя досье', config.TOKEN_CRIMINALIST)
    s_m_photo(PHOTO_3)

    # новости 3
    sleep(300)  # 5мин = 300сек
    bot_journalist.news_3()

    # идёт таймер, где ждём позицию от игрока..
    # если приходит раньше, запускаем уровень
    # если опаздывает, то не ждём и запускаем уровень
    sleep(10)
    s_m_pos('У тебя остаётся минут 7, так что давай быстрее', config.TOKEN_CRIMINALIST)
    game_time = timer(int(const["time_3"]) - 8)  # на 7 минут, 3 левел

    # если опоздал, запускаем таймер поиска
    if game_time[0] == 'late':
        s_m('Федералы уже в пути', config.TOKEN_CRIMINALIST)
        s_m_pos('Так что давай быстрее, детектив')

        game_time = timer(5)
        if game_time[0] == 'no late':
            put(f'{config.URL_B}/game', json={'time': game_time[1], 'level': 3}).json()
            sleep(game_time[1] * 60)
    else:
        put(f'{config.URL_B}/game', json={'time': 6, 'level': 3}).json()
        sleep(6 * 60)

    sleep(15)

    # переход к подозреваемым
    s_m('Федералы уже тут, пора уходить', config.TOKEN_POLICE)
    sleep(3)

    # подсказка
    if relationships_bot_criminalist >= 2:
        s_m('Пока федералы не приехали, мы успели обнаружить ещё одну улику', config.TOKEN_CRIMINALIST)
        s_m_pos('Видны замыленные капли крови на ножках стула. Судя по всему, '
                'убийца ударил стулом жертву.')

    # разговор с подозреваемыми
    for i in range(3):
        # помощь
        if i == 2:
            if relationships_bot_criminalist > 2:
                s_m('Я смог отвлечь федералов, давай быстрей последенего опрашивай', config.TOKEN_CRIMINALIST)
                sleep(2)
            else:
                break

        post_info('bot_police', 15, 'Кого выбираем на опрос?')
        count = wait_answer()  # выбираем кого опрашиваем

        # диалоги с подозреваемыми
        if count == 1:  # диалог - свидетильница смерти жертвы (46 - 49)
            post_info('bot_talks', 46, 'Здравствуйте, я Свидетильница. В тот момент я проходила мимо')
            if wait_answer() == 0:
                post_info('bot_talks', 47, 'Но мне кажется, это не случайная смерть')
                if wait_answer() == 0:
                    post_info('bot_talks', 48, 'Больше ничего не могу сказать')
                    wait_answer()
                else:
                    post_info('bot_talks', 48, 'Только уже само падение')
                    wait_answer()
            else:
                post_info('bot_talks', 49, 'Я естественно перепугалась и вызвала полицию')
                if wait_answer() == 0:
                    post_info('bot_talks', 48, 'Я больше ничего не видела и не знаю')
                    wait_answer()
                else:
                    post_info('bot_talks', 48, 'Больше я ничего не знаю')
                    wait_answer()

        elif count == 2:  # диалог - муж (50 - 54)
            post_info('bot_talks', 50, 'Добрый день, Детектив. Я муж погибшей')
            if wait_answer() == 0:
                post_info('bot_talks', 51, 'Но уже возвращался, когда мне позвонила полиция')
                if wait_answer() == 0:
                    post_info('bot_talks', 52, 'Ничего не знаю')
                    wait_answer()
                else:
                    post_info('bot_talks', 53, 'Это очень сильная потеря для меня...')
                    wait_answer()
            else:
                post_info('bot_talks', 54, 'Всегда была аккуратной')
                if wait_answer() == 0:
                    post_info('bot_talks', 53, 'Но то что вернусь я, она не знала')
                    wait_answer()
                else:
                    post_info('bot_talks', 53, 'Но в тот день она не должна была прийти')
                    wait_answer()

        else:  # диалог - Подруга (55 - 60)
            post_info('bot_talks', 55, 'Хай, я подруга Инна. Вызывали?')
            if wait_answer() == 0:
                post_info('bot_talks', 56, 'Я вообще удивлина что она полезламыть окна'
                                           ', так что это точно подстава от своих')
                if wait_answer() == 0:
                    post_info('bot_talks', 57, 'но она стала покупать какие-то препараты и гворила то'
                                               ' если скажет гле покупает, она будет мертва ')
                    if wait_answer() == 0:
                        post_info('bot_talks', 58, 'Она слово закон, на неё можно положиться')
                        wait_answer()
                    else:
                        post_info('bot_talks', 58, 'Ничего такого, обычное дело понимаешь?')
                        wait_answer()
                else:
                    post_info('bot_talks', 59, 'Говорила, что это из-за своей дурацкой работы. Такая вот она рабочая')
                    if wait_answer() == 0:
                        post_info('bot_talks', 58, 'Я не интересовалась')
                        wait_answer()
                    else:
                        post_info('bot_talks', 58,
                                  'Я конечно хотела узнать где она берёт эту дрянь, но так и не узнала')
                        wait_answer()
            else:
                post_info('bot_talks', 60, 'Она не была из тех, кто любил тусить или тем более изменять')
                if wait_answer() == 0:
                    post_info('bot_talks', 58, 'Она не отдыхала. Больше я ничего не знаю')
                    wait_answer()
                else:
                    post_info('bot_talks', 58, 'Больше не знаю')
                    wait_answer()

    post_info('bot_police', 16, 'Ну что скажешь, есть ли подозреваемые?')

    if wait_answer() == 0:
        s_m(
            'Мы задердали ее до конца расследования\nВот её алиби: Я с ней разговаривала по телефону утром, сказала, '
            'что еду к маме. Больше мы не связывались. От мамы я выехала где-то в 13:25-13:30, ехать около часа',
            config.TOKEN_POLICE)
        suspect.append('Подруга, Инна')

    else:
        s_m('Мы задержали его, до конца расследования\nЕго алиби: Да, не спорю, это странно, что я вернулся раньше.'
            ' Но это правда. Командировка закончилась раньше, я сменил билеты, взял новые, и раньше вылетел. '
            'Когда подъезжал к цветочному магазину мне позвонили и сказали, что моя жена мертва. Я сразу же поехал '
            'сюда. Клянусь, это был не я.»', config.TOKEN_POLICE)
        suspect.append('Муж')

    sleep(10)

    s_m('Так, ну пока у нас затишье можешь взглянуть на всё происходящие и подумать')

    sleep(120)  # 120сек = 2мин

    # незнакомец
    s_m('Я знаю, кто убийца', config.TOKEN_ANONYM)
    sleep(3)
    s_m('Это не просто самоубийства или случайности')
    sleep(4)
    s_m('Есть один человек, торгует наркотой, вот это сделал он. Я у него какое-то время брал дозу,'
        ' но потом закончил...')
    sleep(4)
    post_info('bot_anonym', 0, 'Имя вроде бы Стас, рост под 178-180, тусуется всегда в баре на Молокова. Там найдете')

    if wait_answer() == 0:
        post_info('bot_anonym', 1, 'Я буду мёртв')
        if wait_answer() == 0:
            post_info('bot_anonym', 2, 'Абсолютно')
            wait_answer()
        else:
            post_info('bot_anonym', 2, 'Но я правда хочу Вам помочь')
            wait_answer()
    else:
        post_info('bot_anonym', 3, 'Абсолютно')
        if wait_answer() == 1:
            post_info('bot_anonym', 2, 'Но я правда хочу Вам помочь')
            wait_answer()

    sleep(5)

    # спрашивает про новсоти, диалог
    post_info('bot_police', 17, 'Новостей пока нет, у вас есть что-нибудь, детектив?')
    time_relationships = wait_answer()
    if time_relationships == 1:
        s_m('Пока криминалист отправит вам досье', config.TOKEN_POLICE)
    elif time_relationships == 3:
        s_m('Хорошо, сейчас всё сделем', config.TOKEN_POLICE)
    elif time_relationships == 2:
        post_info('bot_police', 18, 'Даже если он наврал, то нам это никак не навредит')
        if wait_answer() == 1:
            sleep(3)
            s_m('Скидываю досье', config.TOKEN_CRIMINALIST)
            s_m_photo(PHOTO_4)
            sleep(10)
            s_m('Детектив, мои люди задержали подозреваемого. Как и говорилось, он был в баре',
                config.TOKEN_POLICE)
    else:
        post_info('bot_police', 18, 'У тебя есть какая-то информация?')
        if wait_answer() == 1:
            sleep(3)
            s_m('Скидываю досье', config.TOKEN_CRIMINALIST)
            s_m_photo(PHOTO_4)
            sleep(10)
            s_m('Детектив, мои люди задержали подозреваемого. Как и говорилось, он был в баре',
                config.TOKEN_POLICE)

    suspect.append("Совкин Станислав Максимович")

    sleep(5)
    # разговор с подозреваемым 61 - 63
    post_info('bot_talks', 61, 'Я ничего не делал, за что вы меня задержали!?')
    if wait_answer() == 0:
        post_info('bot_talks', 62, 'Клянусь!')
        if wait_answer() == 0:
            post_info('bot_talks', 63, 'Но я никого не убивал!')
            wait_answer()
    else:
        post_info('bot_talks', 63, 'Но я никого не убивал!')
        wait_answer()

    # ----ЧЕТВЁРТОЕ УБИЙСТВО----

    # заявление о новом убийстве
    s_m_admin('Начинается четвёртое убийство')

    s_m('Детектив! нет времени , пора выезжать', config.TOKEN_POLICE)
    sleep(2)
    s_m('У нас произошло новое убийство.')
    sleep(3)
    s_m('Убита юная девушка 19 лет в районе Весны города Красноярска. '
        'Предположительная причина смерти: асфиксия дыхательных путей.')
    sleep(1)
    s_m(f'Время смерти: {dt.date.today().strftime("%d.%m.%Y")}, '
        f'{(dt.datetime.now() - dt.timedelta(minutes=10)).strftime("%H:%M")}')
    sleep(3)
    s_m(f'Вам надо срочно выезжать на улица {const["point_4"]}. У нас как всегда нет много времени.'
        ' Вам также скоро скинут досье на жертву',
        config.TOKEN_POLICE)

    sleep(60)  # 1мин - 60сек

    # досье
    s_m('Ваше досье, детектив', config.TOKEN_CRIMINALIST)
    s_m_photo(PHOTO_5)

    sleep(180)  # 3мин = 180сек

    # 4 Новости
    bot_journalist.news_4()

    # идёт таймер, где ждём позицию от игрока..
    # если приходит раньше, запускаем уровень
    # если опаздывает, то не ждём и запускаем уровень
    sleep(10)
    s_m_pos('Время идёт, поторопись!', config.TOKEN_CRIMINALIST)
    game_time = timer(int(const['time_4']) - 4)  # на 10 минут, 4 левел

    # если опоздал, запускаем таймер поиска
    if game_time[0] == 'late':
        s_m('Время уже идёт!', config.TOKEN_CRIMINALIST)
        s_m_pos('Давай быстрее')

        game_time = timer(5)
        if game_time[0] == 'no late':
            put(f'{config.URL_B}/game', json={'time': game_time[1], 'level': 4}).json()
            sleep(game_time[1] * 60)
    else:
        put(f'{config.URL_B}/game', json={'time': 6, 'level': 4}).json()
        sleep(6 * 60)

    sleep(10)

    post_info('bot_police', 19, 'Всё, пора уходить. Сам понимаешь почему...\nНенавижу их. Всегда мешают работать!')
    relationships_bot_police += wait_answer()

    sleep(2)
    s_m('Пришло время опрашивать людей', config.TOKEN_POLICE)

    # разговор с подозреваемыми
    for i in range(3):
        # помощь
        if i == 2:
            if relationships_bot_police >= 3:
                s_m('Давай опросим последнего. Я смог его забрать у них. Только тихо, иначе вставят.',
                    config.TOKEN_POLICE)
            else:
                break

        post_info('bot_police', 20, 'Кого опросим?')  # отдаём через файл команду полицаю
        count = wait_answer()  # выбираем кого опрашиваем

        # диалоги с подозреваемыми
        if count == 1:  # диалог - тётя (64 - 67)
            post_info('bot_talks', 64, 'Я тётя Софии. Готова отвечать на ваши вопросы')
            if wait_answer() == 0:
                post_info('bot_talks', 65, 'Но особо не придавала этому значения')
                if wait_answer() == 0:
                    post_info('bot_talks', 66, 'Она ведь уже далеко не маленькая девочка. Больше ничего такого')
                    wait_answer()
                else:
                    post_info('bot_talks', 66, 'Неа, больше ничего не знаю')
                    wait_answer()

            else:
                post_info('bot_talks', 67, 'Я знала о том, что она далеко не пай-девочка, '
                                           'но не могла ей ничего запрещать, она ведь уже далеко не маленькая девочка')
                if wait_answer() == 0:
                    post_info('bot_talks', 66, 'Всё, больше не знаю')
                    wait_answer()
                else:
                    post_info('bot_talks', 66, 'Больше ничего')
                    wait_answer()

        elif count == 2:  # диалог - лучшая подруга (68 - 72), 66
            post_info('bot_talks', 68, 'Приветсвую, я лучшая подруга Сони')
            if wait_answer() == 0:
                post_info('bot_talks', 69, 'Вот постоянно отшивает парней')
                if wait_answer() == 0:
                    post_info('bot_talks', 66, 'Больше ничего не знаю')
                else:
                    post_info('bot_talks', 70, 'Но где-то с полгода назад она начала тесно с кем-то общаться')
                    if wait_answer() == 0:
                        post_info('bot_talks', 66, 'Скажу точно, он мне не понравился, лицо его. Не доброе оно')
                        wait_answer()
                    else:
                        post_info('bot_talks', 66, 'Особо о нём она не говорила, и тем более не показывала')
                        wait_answer()
            else:
                post_info('bot_talks', 71, 'Но в последенее время стала тесно общаться с кем-то')
                if wait_answer() == 0:
                    post_info('bot_talks', 66, 'Особо о нём она не говорила, и тем более не показывала.'
                                               ' А катался он на тонированой машине')
                    wait_answer()
                else:
                    post_info('bot_talks', 66, 'Вид у него не добрый')
                    wait_answer()

        else:  # диалог - свидетильница (72 - 73)
            post_info('bot_talks', 72, 'Так, здравствуйте, я свидетильница. Была поблизости')
            if wait_answer() == 0:
                post_info('bot_talks', 73, 'Больше я ничего не знаю... Это было быстро')
                wait_answer()
            else:
                post_info('bot_talks', 73, 'Тут же позвонила в скорую. Больше я ничего не знаю')
                wait_answer()

    sleep(3)

    # мини диалог (21, 22), выбор подозреваемого
    s_m('Хм, тут всё странно...', config.TOKEN_POLICE)
    post_info('bot_police', 21, 'Думаешь тут есть вообще подозреваемые?')
    relationships_bot_police += wait_answer()

    post_info('bot_police', 22, 'Жду')

    time_relationships = wait_answer()
    if time_relationships == 1:
        s_m('Алиби: "Мне так сложно говорить, простите. Я была на работе,'
            ' проверяла наличие товара на складе, работала с самого утра"')
        suspect.append('Тётя')
    elif time_relationships == 2:
        s_m('Подругу выбрал... Хорошо, мы задержим её\nАлиби: "Я её любила даже больше, чем просто подругу. Она была '
            'мне гораздо ближе, это была какая-то любовь. Но я её не убивала, клянусь. '
            'Я была в спортзале с 4х часов, в течение двух часов"')
        suspect.append('Подруга, Алиса')
    else:
        s_m('Мне кажется, ты сделал правильный выбор. Молодец')

    sleep(8)

    # Секретный чат, кримналист
    s_m('Мы нашли символы на руке. Пока ты разговаривал, я разгадал шифр. Это секретный чат. '
        'Я его сейчас активирую и тебе должен кто-то написать.  Жди', config.TOKEN_CRIMINALIST)

    sleep(7)

    # гадалка
    s_m('Привет', config.TOKEN_FORTUNETELLER)
    sleep(2)
    post_info('bot_fortuneteller', 0, 'Ты разгадал мою загадку')

    count = wait_answer()
    if count == 0:
        post_info('bot_fortuneteller', 1, 'Другой вопрос, кто ты такой')
        wait_answer()

    post_info('bot_fortuneteller', 2, 'Допустим')
    wait_answer()

    s_m('Но это имя мне знакомо')
    sleep(1)
    s_m('Что-то не так?')
    sleep(3)
    post_info('bot_fortuneteller', 4, 'Будьте честны со мной, и я буду честна с вами')

    count = wait_answer()
    if count == 0:
        s_m('Не могу рассказать всё, иначе сама буду в опасности, но могу сказать точно, что это не тот,'
            ' кого вам подсказали')
        post_info('bot_fortuneteller', 5, 'Это всё')
        wait_answer()
    else:
        post_info('bot_fortuneteller', 6, 'Мы давно не общались')
        wait_answer()

    sleep(3)

    # криминалист
    s_m('Я вижу, что чат закрыт. Хотелось бы спросить что было, но нам уже сообщили о новом убийстве',
        config.TOKEN_CRIMINALIST)
    s_m('Пойду готовить досье')

    # ----ПЯТОЕ УБИЙСТВО----

    # о новом убийстве
    s_m_admin('Начинается пятое убийство')

    sleep(5)

    s_m('Произошло очередное убийство! Это уже 5, пора заканчивать дело!!!', config.TOKEN_POLICE)
    sleep(2)
    s_m(f'Убит мужчина 27 лет в собственной квартире, в районе {const["zone_5"]} Предположительная причина смерти:'
        ' передозировка инсулином.')
    sleep(1)
    s_m(f'Время смерти: {dt.date.today().strftime("%d.%m.%Y")}, '
        f'{(dt.datetime.now() - dt.timedelta(minutes=1)).strftime("%H:%M")}')
    sleep(2)
    s_m(f'Выдвигайся к {const["point_5"]}')
    s_m(f'На этот раз у нас {const["time_5"]} мин')

    sleep(60)  # 50сек = 1мин

    # досье
    s_m('Досье для пятого убийства', config.TOKEN_CRIMINALIST)
    s_m_photo(PHOTO_6)

    sleep(120)  # 120 = 2мин

    # 5 новости
    bot_journalist.news_5()

    # идёт таймер, где ждём позицию от игрока..
    # если приходит раньше, запускаем уровень
    # если опаздывает, то не ждём и запускаем уровень
    sleep(10)
    s_m_pos('Всё как обычно, поторопись до места пресступления', config.TOKEN_CRIMINALIST)
    game_time = timer(int(const["time_5"]) - 3)  # на 10 минут, 5 левел

    # если опоздал, запускаем таймер поиска
    if game_time[0] == 'late':
        s_m('Время уже идёт!', config.TOKEN_CRIMINALIST)
        s_m_pos('Давай быстрее')

        game_time = timer(5)
        if game_time[0] == 'no late':
            put(f'{config.URL_B}/game', json={'time': game_time[1], 'level': 5}).json()
            sleep(game_time[1] * 60)
    else:
        put(f'{config.URL_B}/game', json={'time': 6, 'level': 5}).json()
        sleep(6 * 60)

    sleep(10)

    s_m('Снова федералы...', config.TOKEN_POLICE)
    sleep(2)
    s_m('Ну что, идём разговаривать и снова с ограничением из-за федералов...')

    # разговор с подозреваемыми
    for _ in range(2):
        post_info('bot_police', 24, 'Кого берёшь?')  # отдаём через файл команду полицаю
        count = wait_answer()  # выбираем кого опрашиваем

        # диалоги с подозреваемыми
        if count == 1:  # диалог - Невеста (74 - 76)
            post_info('bot_talks', 74, 'День добрый, я невеста Влада, Кира')
            if wait_answer() == 1:
                post_info('bot_talks', 75, 'Меня охватила паника, ужас, шок!')
                if wait_answer() == 1:
                    post_info('bot_talks', 76, 'Всегда был абсолютно адекватен, я..я не знаю, что могло произойти и '
                                               'что он мог принимать, как мог спутать дозы…')
                    wait_answer()
                else:
                    post_info('bot_talks', 76, 'Он очень ответственный человек')
                    wait_answer()
            else:
                post_info('bot_talks', 75, 'Всё как обычно')
                if wait_answer() == 1:
                    post_info('bot_talks', 76, 'Всегда был абсолютно адекватен, я..я не знаю, что могло произойти и '
                                               'что он мог принимать, как мог спутать дозы…')
                    wait_answer()
                else:
                    post_info('bot_talks', 76, 'Он очень ответственный человек')
                    wait_answer()

        elif count == 2:  # диалог - лучший друг (77 - 80)
            post_info('bot_talks', 77, 'Всем привет. Илья, лучший друг Влада')
            if wait_answer() == 1:
                post_info('bot_talks', 78, 'Но толком ничего не сказал... Это всё пожалуй')
                if wait_answer() == 1:
                    post_info('bot_talks', 79, 'Он очень ответственный')
                    wait_answer()
                else:
                    post_info('bot_talks', 79, 'Но парой может что-то утаить')
                    wait_answer()
            else:
                post_info('bot_talks', 80, 'При этом всегда доставал дозу он')
                if wait_answer() == 1:
                    post_info('bot_talks', 79, 'Нам это не собо понравилось')
                    wait_answer()
                else:
                    post_info('bot_talks', 79, 'Та ещё дрянь')
                    wait_answer()

        else:  # диалог - Отец (81 - 85)
            post_info('bot_talks', 81, 'Здравствуйте. Я отец Влада')
            if wait_answer() == 1:
                post_info('bot_talks', 82, 'Я с ним был ближе чем мать')
                if wait_answer() == 1:
                    post_info('bot_talks', 83, 'Также отвесным и серьёзным')
                    wait_answer()
                else:
                    post_info('bot_talks', 85, 'Вот...')
                    if wait_answer() == 0:
                        post_info('bot_talks', 83, 'То показалось странным и даже подозрительным')
                        wait_answer()
                    else:
                        post_info('bot_talks', 83, 'Да и он не говорил ничего')
                        wait_answer()
            else:
                post_info('bot_talks', 84, 'Это показалось странным и даже подозрительным')
                if wait_answer() == 0:
                    post_info('bot_talks', 83, 'Да и он не говорил ничего')
                    wait_answer()
                else:
                    post_info('bot_talks', 83, 'Также отвесным и серьёзным')
                    wait_answer()

    sleep(4)
    s_m('Ну что скажаешь?', config.TOKEN_POLICE)
    post_info('bot_police', 25, 'Кто подозреваемый?')

    if wait_answer() == 0:
        s_m('Её алиби: «Я вернулась домой от подруги, зашла, а там лежит он… Меня охватила паника, ужас, шок. '
            'Как только чуть успокоилась, вызвала полицию. Он никогда не пропускал приём инсулина, и тем более, '
            'не могу случайно спутать дозы. Это невозможно, он относился к этому с полной ответственностью. Всегда '
            'был абсолютно адекватен, я..я не знаю, что могло произойти и что он мог принимать, как мог спутать дозы…»')
        suspect.append('Кира, невеста')

    else:
        s_m('Его Алиби: «По приколу пару раз употребляли, но мы лишь баловались, при этом всегда доставал'
            ' дозу он. Но всегда был в себе, а лекарство тем более не пропускал. После пары раз больше не пробовали. В'
            ' последнее время он стал более скрытный, говорил, что переживает за Киру, да и за свою жизнь. Но толком'
            ' ничего не сказал.»')
        suspect.append('Друг, Илья')

    sleep(3)

    s_m('Думаю пришло время уже что-то делать. У нас 5 убийство и есть подозреваемые')
    s_m('Предлогаяю сопоставить все данные и выбрать убийцу...')
    sleep(2)
    s_m('Сейчас тебе криминалист скинет по всем подозреваемым досье\nТы должен подумать. '
        'Скоро я тебе напишу и спрошу что ты думаешь...')

    sleep(3)
    s_m('Сейчас отправлю досье всех подозреваемых, кого ты задержал', config.TOKEN_CRIMINALIST)
    for i in suspect:
        sleep(20)
        s_m('---')
        if i == 'Подруга, Инна':
            s_m('Подруга, Инна')
            s_m('Подруга убитой, Маниулина Инна Владимировна,38 лет, 24.05.1982.'
                ' Уроженка города Красноярск. Окончила 9 классов городской школы и поступила в '
                'медицинский колледж на медсестру. Закончив колледж, нашла работу медсестры в '
                'частной клинике. Родителей нет. Бабушка и дедушка живут на окраине города, с '
                'девушкой видятся редко. Не замужем, детей нет. Отсутствуют судимости, братья и сестры.')
        elif i == 'Муж':
            s_m('Муж')
            s_m('Муж убитой, Эйснер Антон Антонович,39 лет, 01.12.1981. '
                'Уроженец города Москва. Родители живы, проживают в Красноярске.'
                ' В возрасте 3х лет был вынужден переехать с родителями в Красноярск '
                'в связи с работой отца, после чего так и не вернулся обратно в родной город.'
                ' Отучился в красноярском лицее, после чего, уйдя после 11 класса, поступил на '
                'бухгалтера. Стал работать в Красноярской Мебельной Компании, после чего был повышен'
                ' до директора фирмы. Со своей женой познакомился во время поездки в Германию. После '
                'сыграли свадьбу в Германии, затем переехали в Красноярск. Детей нет, судимостей нет, '
                'периодически уезжает в командировки по работе. ')
        elif i == 'Хозяйка собаки':
            s_m('Хозяйка собаки')
            s_m('Хозяйка собаки, Ищенко Дарья Игнатовна, 26 лет, 26.05.1994.'
                ' Уроженка города Красноярск. Окончила среднюю школу, ушла после 9 класса в колледж '
                'на тренера по дзюдо. Отучилась, в данный момент работает тренером в детском центре. '
                'Была собака, но та умерла из-за конфуза во время операции в ветеринарной клинике. '
                'Единственный ребенок в семье, родители умерли, родных и близких нет. Живет в '
                'однокомнатной квартире. Судимостей нет.')
        elif i == 'Жена':
            s_m('Жена')
            s_m('Жена убитого, Авдеева (Бойкина) Алена Ярославовна, 35 лет, 08.07.1985. '
                'Уроженка города Красноярск. Есть двое детей-близнецов 5 лет. Единственный ребенок в '
                'семье, родители живы, проживают в загородном доме за Красноярском. Образование девушка '
                'получила в Гимназии города Красноярск, окончила 11 классов, затем поступила в '
                'университет на психолога, выпустилась из университета с отличием. В скором времени '
                'познакомилась со своим будущим мужем. В 29 лет вышла замуж, спустя год родила двух '
                'детей. Работает психологом крупной конторе.')
        elif i == 'Подруга, Алина':
            s_m('Подруга, Алина')
            s_m('Подруга убитой, Зейненко Алина Ивановна, 22 года, 21.10.1998. '
                'Уроженка города Красноярск, родилась в многодетной семье, была самым '
                'младшим ребенком. Обучалась в одной из школ до 10 лет, из-за травли пришлось'
                ' перевестись в другую, где девушка доучилась до 11 класса. Окончила школу с одной'
                ' четверкой по математике, затем поступила на повара-кондитера. Ранее состояла в '
                'отношениях с молодым человеком по имени Вячеслав, но прекратили отношения спустя долгое'
                ' время. Родители живы, проживают в Красноярске. Сама девушка проживает в общежитии, '
                'где и познакомилась с убитой. Являлась соседкой по комнате убитой. Есть сестра Ирина-16 '
                'лет, проживает с родителями.')
        elif i == 'Парень':
            s_m('Парень')
            s_m('Парень убитой, Ханин Олег Богданович, 24 года, 13.01.1996. Уроженец города '
                'Саяногорск. Получал образование все 11 лет в Саяногорской школе, окончил школу с '
                'красным аттестатом, затем поступил в Красноярский университет на экономиста. Мать '
                'умерла, когда мальчику было 10, отец ушел из семьи при рождении Олега, всю оставшуюся '
                'жизнь мальчика воспитывала бабушка, в данный момент живущая в Саяногорске. Со своей '
                'девушкой Еленой Олег познакомился в кафе, долгое время состояли в отношениях. Снимает '
                'квартиру в центре города, каждые три месяца приезжает к бабушке в Саяногорск,'
                ' подрабатывает доставщиком еды в распространённой фирме, чем зарабатывает себе на жизнь.'
                ' Братьев и сестер нет.')
        elif i == 'Совкин Станислав Максимович':
            s_m('Совкин Станислав Максимович')
            s_m('Совкин Станислав Максимович, 25 лет, 15.12.1995 г.р. Нет родных, все близкие мертвы. '
                'Был отправлен в детский дом в возрасте пяти лет. Имел знакомство с курением и проблемами'
                ' с алкоголем. Стоял долгое время на учете в милиции за алкоголь и воровство. В 18 лет'
                ' покинул пределы детского дома, начал развивать собственную торговлю незаконными '
                'веществами. Стал мелким дилером, занимался этим долгое время, после чего завязал '
                'из-за неудачной ситуации. Не имеет образования помимо окончания 9 классов. Никаких '
                'заболеваний в медицинской карте нет. Братьев и сестер нет, семью не видел с детства.')
        elif i == 'Тётя':
            s_m('Тётя')
            s_m('Тетя убитой, Шашина Марианна Кирилловна, 50 лет, 06.09.1970. '
                'Уроженка поселка Песчанка, окончила сельскую школу и поступила в Красноярский колледж '
                'на предпринимателя.  Есть двое детей, 25 и 23 года, обе девочки. После окончания '
                'колледжа какое-то время проходила практику в городе, затем устроилась на работу. '
                'Проживает одна на окраине города. С недавних пор жила в одной квартире с племянницей. '
                'Муж умер от инфаркта в возрасте 45 лет. Судимостей нет, братья и сестры отсутствуют.')
        elif i == 'Лучшая подруга, Алиса':
            s_m('Лучшая подруга, Алиса')
            s_m('Лучшая подруга убитой, Осипова Алиса Витальевна, 19 лет, 15.04.2000. '
                'Уроженка города Красноярск. Родители живы, есть младшая сестра 10 лет и брат 13 лет, '
                'все живут в центре города. Окончила Красноярскую школу, после 9го класса выбрала'
                ' биохимическое направление в 10-11 класс. После окончания школы поступила в '
                'университет, выбрав профессию микробиолога. С убитой познакомилась на лекциях, '
                'сильно сдружились. Личная жизнь отсутствуют, судимости отсутствуют.')
        elif i == 'Кира, невеста':
            s_m('Кира, невеста')
            s_m('Невеста убитого, Зоева Кира Алексеевна, 27 лет, 15.09.1993.'
                ' Уроженка города Красноярска. Родители живы, бабушка и дедушка тоже, '
                'есть старший брат Даниил. Родители проживают в Нижнем Новгороде, переехали туда около'
                ' года назад. Старший брат 29 лет живет в Москве. Кира окончила Красноярский лицей, '
                'затем поступила на фармацевта. Спустя год после обучения в университете нашла свою '
                'любовь, спустя несколько лет вышла замуж. '
                'Семья была обеспечена, поэтому Кира не стала работать по профессии, став домохозяйкой. '
                'Часто контактирует с братом, несмотря на большое расстояние. Отсутствуют судимости, дети.')
        elif i == 'Друг, Илья':
            s_m('Друг, Илья')
            s_m('Друг убитого, Миронов Илья Данилович, 28 лет, 06.07.1992.'
                ' Уроженец города Екатеринбург. В возрасте 7 лет переехал с матерью от отца в Красноярск,'
                ' где и остался жить и учиться. Получал обучение в обычной средней школе.'
                ' Ушел после 11 класса дабы обучиться на химика. От его лица было подано 4 заявления в разные'
                ' институты., приняли только в один. Со своим лучшим другом Илья познакомился на вечеринке у их '
                'общего знакомого, с тех пор сдружились. Мать Ильи проживает в Красноярске, отец в Екатеринбурге.'
                ' Сам Илья снимает квартиру недалеко от института. Также Илья работает на полставки в одной из фирм,'
                ' делающих поставки определенных товаров в больницы, аптеки и т.д. В детстве увлекался мифологией,'
                ' верующий. Считает, что у всего есть карма, ангелы и демоны, а также ад и сам Сатана.'
                ' Никаких заболеваний в медицинской карте нет.'
                ' Имеет хорошее химическое образование, победитель многих олимпиад по химии и органике.')

    sleep(10)
    s_m('Это всё. Сделай правильный выбор. У тебя есть время подумать')

    sleep(180)  # 3 мин = 180 сек

    # отрытия решения
    post_info('bot_police', 26, 'Всё, время пришло. Готов?')  # отдаём через файл команду полицаю
    wait_answer()

    # концовка
    s_m_admin('концовка')
    s_m('Напиши, кто по твоему убийца? Пиши имя также, как тебе писал Криминалист!', config.TOKEN_POLICE)

    get_g = get(f'{config.URL_B}/game').json()
    get_g['items'] = [suspect]
    post(f'{config.URL_B}/game', json=get_g)

    if wait_answer() == 1:
        for i in range(3):
            s_m('XXX',  config.TOKEN_POLICE)
            s_m('XXX', config.TOKEN_CRIMINALIST)
            s_m('XXX', config.TOKEN_ANONYM)
            s_m('XXX', config.TOKEN_FORTUNETELLER)
            s_m('XXX', config.TOKEN_TALKS)
            s_m('XXX', config.TOKEN_JOURNALIST)
            sleep(1)
        sleep(10)
        bot_journalist.news_end1()

    else:
        for i in range(3):
            s_m('XXX', config.TOKEN_POLICE)
            s_m('XXX', config.TOKEN_CRIMINALIST)
            s_m('XXX', config.TOKEN_ANONYM)
            s_m('XXX', config.TOKEN_FORTUNETELLER)
            s_m('XXX', config.TOKEN_TALKS)
            s_m('XXX', config.TOKEN_JOURNALIST)
            sleep(1)
        sleep(10)
        bot_journalist.news_end2()

    s_m_admin('Конец игры')


def main():
    with open('json/const_game.json', encoding='utf-8') as file:
        data = json.load(file)['Молокова']  # input()

    game(data)


if __name__ == '__main__':
    main()
