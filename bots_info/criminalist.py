# список [ответов игрока, ответов персонажа, зависимоть отношения]
criminalist_info = [
    [
        # 0, вступление
        ['Кто? впервые слышу...', 'Ничего нового', 0],
        ['Хорошо, я запомню. Спасибо!', 'Также скажу, что улики могут быть в любом месте.'
                                        ' Чем больше найдешь, тем легче будет понять происходящее\n'
                                        'Удачи тебе)', 1],
        ['Уяснил. Спасибо, но лучше бы ты молчал, помощник', 'Я подозревал такое... Ладно, удачи тебе\n'
                                                             'Всё равно буду рад помочь тебе', -1],
        ['Да пошёл ты!', 'Я подозревал такое... Ладно, удачи тебе\n'
                         'Всё равно буду рад помочь тебе', -1],
    ],
    [
        # 1
        ['Да иди ты', 'Мда...', -1],
        ['Ну бывает, извиняй', 'Спасибо хоть на этом... Удачи там, поторопись', 1],
        ['Постараюсь тебя вспомнить, а то башка раскалывается...', 'Спасибо хоть на этом... Удачи там, поторопись', 1],
        ['Держи в курсе', 'Постараюсь', 0],
    ],
    [
        # 2, диалог + подсказка
        ['Она мне показалось подозрительной', 'М?', 0],
        ['Не суй свой нос куда не надо', 'Я лишь хотел спросить и узнать... Мне кажется это не она... Ладно', -1],
        ['На это есть определённые показания...Странная она', 'а...', 0],
        ['Мне  подсказала интуиция', 'А...', 1],
    ],
    [
        # 3
        ['Тебе какая разница то? Если хочешь помочь,'
         ' то не надо. Лучше иди и занимайся своей работой', 'Я хотел только помочь... '
                                                             'Мне кажется это не она и всё... Ладно', -1],
        ['А что такое?', 'Мне кажется, что это не она...', 1],
        ['Я не верю ей. Говорила не правильно... Мне кажется, врёт она, что не злится на него', 'Думаешь так?', 2],
        ['Она зачем-то рассказала про наркотики, хотела отвести от себя подозрения', 'Она лишь хотела помочь нам', 3],
    ],
    [
        # 4
        ['Она гвоорила как-то подозрительно, мне кажется, она врёт', 'Думаешь так?', 1],
        ['Он отводила от себя подозрения, поэтому она может быть виновной', 'Она лишь хотела помочь нам', 2],
        ['Да она убийца и всё. Не лезь', 'Просто мне кажется, что это не она. Жена более подозрительная.', -1],
        ['Она зла на него, всяко она хотела его убить.'
         ' Из-за него погиб её любимый друг! Многие после такого сходят с ума', 'Она не из этих', 3],
    ],
    [
        # 5
        ['Жена... Думаешь так?', 'Да. Я конечно понимаю, жена и все дела...', 0],
        ['Слушай, наверное ты прав... Я поменяю своё выбор', 'Круто! Надеюсь мы правы', 1],
        ['Что ты гворишь? Сам себе не ври\nЗря только слушал тебя', 'Делай как знаешь,  я только хотел помочь', -1],
        ['Ну не знаю... Спасибо конечно, но я не буду что-то менять', 'Хорошо, дело твоё.'
                                                                      ' Детектив тут ты, но всё же подумай', 1],
    ],
    [
        # 6
        ['Хм... Ладно, спасибо, я подумаю', 'Хорошо, спасибо', 1],
        ['Да не, не думаю. Я ничего не буду менять', 'Хорошо, как знаешь. Но подумай ещё раз', 0],
        ['Неее, бред. Зря только выслушала тебе. ', 'Как знаешь...', -1],
        ['Звучит не совем убедительно. Я лучше останусь при своём мнение', 'Ладно, но подумай ещё раз', 0],
    ],
    [
        # 7
        ['Да, тебе не понять', 'Лан,... но я бы на твоём месте пересмотрел выбор', 1],
        ['Да не зацикливайся. Это мои тараканы, понимай', 'Знаю... Есть у тебя такое\n'
                                                          'Хорошо, только ещё раз подуйма над этим', 0],
        ['Надоел уже. Давай без всяких вопросов. Иди работай', 'Ничего нового.. Просто подумай'
                                                               ' ещё раз над своим выбором', -1],
        ['Не только, но а что такое?\nТы думаешь иначе?', 'Да, мне кажется жена более подозрительная,'
                                                          ' чем это женщина', 0],
    ],
    [
        # 8
        ['Хм...  Я подумаю', 'Хорошо, спасибо', 1],
        [' Я ничего не буду менять. Мне кажется ты не прав', 'Хорошо, как знаешь. Но подумай ещё раз', 0],
        ['Неее, бред. зря только выслушал тебе', 'Как знаешь...', -1],
        ['Это всего догадки...', 'Ладно, но подумай ещё раз', 0],
    ],
    [
        # 9
        ['', '', 0],
        ['', '', 0],
        ['', '', 0],
        ['', '', 0],
    ],
    # фразы, если нет такого ответа от игрока в нашем сюжете
    [
        'Не понимаю...', 'Повтори ещё раз', 'Слушаю тебя'
    ]
]