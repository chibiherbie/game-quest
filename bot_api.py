from flask_restful import reqparse, abort, Api, Resource
from flask import Flask, jsonify
import json

from _data import db_session
from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('isActive', required=True, type=bool)
parser.add_argument('num_block', required=True, type=int)
parser.add_argument('text', required=True)


app = Flask(__name__)
api = Api(app)


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
        bots = {
          "bot_police": {
            "num_block": 0,
            "text": "",
            "isActive": False
          },
          "bot_admin": {},
          "bot_connect": {
            "num_block": 0,
            "isActive": False,
            "text": ""
          }
        }
        with open('json/main_connect.json') as f:
            json.dump(bots, f)


class GameResource(Resource):
    def get(self):
        with open('json/game_connect.json') as f:
            data = json.load(f)
        return jsonify(data)

    def post(self):
        args = parser.parse_args()
        print(args)


def main():
    api.add_resource(BotsResource, '/api/<bot>')
    api.add_resource(GameResource, '/api/game')
    app.run()


if __name__ == '__main__':
    main()