from flask import Flask, render_template, redirect
from _data import db_session
from forms.user import BookingForm
from _data.users import User
import os
import datetime as dt
import locale
from random import choice


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

locale.setlocale(locale.LC_ALL, "ru_RU.utf8")  # задаем локально для вывода даты на русском

TIME = ['10:00', '11:30', '13:00', '14:30', '16:00', '17:30', '19:00']  # время закрытия игр


@app.route("/", methods=['GET', 'POST'])
def index():
    db_sess = db_session.create_session()

    params = {}
    params['now_date'] = dt.date.today().strftime("%d %B")
    params['week_date'] = (dt.date.today() + dt.timedelta(weeks=1)).strftime("%d %B")
    params['days'] = [(dt.date.today() + dt.timedelta(days=i)).strftime('%d %B %A').split() for i in range(7)]
    params['booking'] = [i[0] for i in db_sess.query(User.dt_start).all()]

    for i in TIME:
        if i < dt.datetime.now().strftime('%H:%M'):
            del_time(i, db_sess)

    form = BookingForm()
    if form.validate_on_submit():
        url = genereta_url()
        user = User(
            name=form.name.data,
            email=form.email.data,
            address=form.address.data,
            dt_start=form.dt_start.data,
            url=url
        )
        db_sess.add(user)
        db_sess.commit()

        return redirect('/')
    return render_template('index.html', params=params, form=form)


def genereta_url():
    while True:
        url = ''.join([choice('qwertyuiopasdfghjklzxcvbnm') for _ in range(10)])
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.url == url).first():
            continue
        break
    return url


def del_time(time, db_sess):
    now = f"{str(int(TIME[TIME.index(time)].split(':')[0]) + 1) + ':' + TIME[TIME.index(time)].split(':')[1]}" \
          f" {dt.date.today().strftime('%d %B %A').lower()}"

    if not db_sess.query(User).filter(User.dt_start == now).first():
        user = User(
            name='ОТМЕНА',
            email='ОТМЕНА',
            address='ОТМЕНА',
            dt_start=now,
            url='ОТМЕНА'
        )

        db_sess.add(user)
        db_sess.commit()
        print('Время закрыто: ', now)


def main():
    db_session.global_init(os.environ.get('DATABASE_URL', 'sqlite:///db/quest.db?check_same_thread=False'))
    port = int(os.environ.get("PORT", 5000))
    # app.run()
    app.run(host='0.0.0.0', port=port)


if __name__ == '__main__':
    main()