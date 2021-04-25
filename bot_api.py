import datetime
from urllib import request

from flask_restful import reqparse, abort, Api, Resource
from flask import Flask, jsonify
import json
from time import sleep
import datetime as dt

from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('isActive', required=True, type=bool)
parser.add_argument('num_block', required=True, type=int)
parser.add_argument('text', required=True)

parser_game = reqparse.RequestParser()
parser_game.add_argument('user_id', required=True, type=str)
parser_game.add_argument('time', required=True, type=int)
parser_game.add_argument('level', required=True, type=int)
parser_game.add_argument('items', required=True, type=list)

parser_time = reqparse.RequestParser()
parser_time.add_argument('time', required=True, type=int)
parser_time.add_argument('level', required=True, type=int)


app = Flask(__name__)
api = Api(app)

TIME, TIME_SEC = 0, 0


# без этого не хотело работать
@app.route('/')
def index():
    return 'empty'


class BotsResource(Resource):
    def get(self, bot):
        with open('json/main_connect.json') as f:
            data = json.load(f)
        return jsonify(data[bot])

    def post(self, bot):
        args = parser.parse_args()

        with open('json/main_connect.json') as file:
            data = json.load(file)

            data[bot]['isActive'] = args['isActive']
            data[bot]['num_block'] = args["num_block"]
            data[bot]['text'] = args["text"]

        with open('json/main_connect.json', 'w') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)

    # перезагружаем файл связи
    def delete(self, bot):
        with open('json/main_connnect-clear.json') as file:
            bots = json.load(file)

        with open('json/main_connect.json', 'w') as file:
            json.dump(bots, file, ensure_ascii=False, indent=2)


class GameResource(Resource):
    def get(self):
        global TIME

        with open('json/game_connect.json') as f:
            data = json.load(f)

        # если запущен таймер
        if TIME != 0:
            t = (dt.datetime.now() - TIME)  # разница во времени
            t = divmod(t.days * 24 * 60 * 60 + t.seconds, 60)  # пеереводим разницу в "мин:сек"
            t = t[0] * 60 + t[1]  # переводим в сек

            # t = f'{t[0]}:{t[1]}'
            # t = sum(int(i) * 60 ** index for index, i in enumerate(t.split(":")[::-1]))  # переводим в секунды

            data['time'] = TIME_SEC - t
            if data['time'] <= 0:
                data['time'] = 0
                data['level'] = 0
                TIME = 0

            with open('json/game_connect.json', 'w') as file:
                json.dump(data, file, ensure_ascii=False, indent=2)

        return jsonify(data)

    def post(self):
        args = parser_game.parse_args()

        with open('json/game_connect.json') as file:
            data = json.load(file)

            data['user_id'] = args['user_id']
            data['time'] = args["time"]
            data['level'] = args["level"]
            data['items'] = args["items"]

        with open('json/game_connect.json', 'w') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)

    def put(self):
        global TIME, TIME_SEC

        args = parser_time.parse_args()

        # запоминаем время начала для таймера
        TIME = dt.datetime.now()

        with open('json/game_connect.json') as file:
            data = json.load(file)

            data['time'] = args["time"] * 60
            data['level'] = args["level"]

        TIME_SEC = data['time']

        with open('json/game_connect.json', 'w') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)

        return


def main():
    api.add_resource(BotsResource, '/api/<bot>')
    api.add_resource(GameResource, '/api/game')

    app.run()


if __name__ == '__main__':
    main()