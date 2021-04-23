from requests import post

post(f'https://chibiherbie.pythonanywhere.com/api/game', json={
        "user_id": "qwerty",
        "time": 10,
        "level": 0,
        "items": [["sdf", "sdf"]]})