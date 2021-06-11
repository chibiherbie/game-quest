import json

FILE = ''


# Ф-ия ищет констаны и меняет их на данные для игры
def edit_text(text, f='../json/const_game.json'):
    global FILE

    if not FILE:
        with open(f, encoding='utf-8') as file:
            FILE = json.load(file)['Молокова']

    if '~' in text:
        text = text.split('~')
        for i in range(len(text)):
            if text[i] in FILE:
                text[i] = FILE[text[i]]

        return ''.join(text)
    return text
