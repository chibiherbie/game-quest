from requests import post, put, get
from config import URL_B

# post(f'https://chibiherbie.pythonanywhere.com/api/game', json={
#         "user_id": "qwerty",
#         "time": 10,
#         "level": 0,
#         "items": [["sdf", "sdf"]]})

# print(get('http://localhost:5000/api/game'))
put(f'{URL_B}/game', json={'time': 1, 'level': 1}).json()

