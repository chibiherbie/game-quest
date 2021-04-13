from flask import Flask, render_template
import os
import datetime as dt
import locale

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

locale.setlocale(locale.LC_ALL, "ru")  # задаем локально для вывода даты на русском


@app.route("/")
def index():
    params = {}
    params['now_date'] = dt.date.today().strftime("%d %B")
    params['week_date'] = (dt.date.today() + dt.timedelta(weeks=1)).strftime("%d %B")
    params['days'] = [(dt.date.today() + dt.timedelta(days=i)).strftime('%d %B %A') for i in range(7)]

    return render_template('index.html', params=params)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run()
    # app.run(host='0.0.0.0', port=port)