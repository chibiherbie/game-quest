# -*- coding: utf-8 -*-
from flask import Flask, render_template, redirect, request
from _data import db_session
from forms.user import BookingForm
from _data.users import User
from random import choice
from mail_sender import send_email, send_email_admin
from dotenv import load_dotenv
import os
import datetime as dt
import locale
import logging
from logging.handlers import RotatingFileHandler


load_dotenv()

application = Flask(__name__)
application.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

locale.setlocale(locale.LC_ALL, "ru_RU.utf8")  # задаем локально для вывода даты на русском

TIME = ['10:00', '11:30', '13:00', '14:30', '16:00', '17:30', '19:00']  # время закрытия игр


# @application.route("/")
# def hello():
#    return render_template('soon.html')


@application.errorhandler(500)
def internal_error(error):
    return render_template('soon.html', error=error)


@application.route("/", methods=['GET', 'POST'])
def index():
    db_sess = db_session.create_session()

    # удаляем время, которые уже прошло
    for i in TIME:
        if i < dt.datetime.now().strftime('%H:%M'):
            del_time(i, db_sess)

    # формируем данные - params
    params = create_session(db_sess)
    print(os.getenv('FROM'))
    form = BookingForm()
    if form.validate_on_submit():
        print(form.dt_start.data)

        params['time'] = form.dt_start.data.split()[0]
        params['date'] = ' '.join(form.dt_start.data.split()[1:])

        # если дата зарегестрирована
        if db_sess.query(User).filter(User.dt_start == form.dt_start.data).first():
            params['message'] = ['Дата уже зарегестрирована', 0]
            return render_template('index.html', params=params, form=form)

        url = genereta_url()
        user = User(
            name=form.name.data,
            email=form.email.data,
            address=form.address.data,
            dt_start=form.dt_start.data,
            url=url
        )
        db_sess.add(user)

        if send_email(form.email.data, form.name.data, form.dt_start.data,
                      form.address.data, f"{request.url}game-id/{url}"):
            db_sess.commit()

            # пересоздаём params с обн. данными
            params = create_session(db_sess)
            print(form.dt_start)
            params['time'] = form.dt_start.data.split()[0]
            params['date'] = ' '.join(form.dt_start.data.split()[1:])
            params['message'] = ['Вы зарегестрировались. На вашу почту отправлено письмо', 1]

            return render_template('index.html', params=params, form=form)

        params['message'] = ['Ошибка', 0]
        return render_template('index.html', params=params, form=form)
    return render_template('index.html', params=params, form=form)


@application.route("/game-id/<url>", methods=['GET', 'POST'])
def game_url(url):
    db_sess = db_session.create_session()

    user = db_sess.query(User).filter(User.url == url).first()
    if user:
        params = {}
        params['message'] = ['', 0]
        params['user'] = user.name
        params['date'] = ' '.join(user.dt_start.split()[1:])
        params['time'] = user.dt_start.split()[0]

        if request.method == 'POST':
            db_sess.delete(user)
            db_sess.commit()
            params['message'] = ['Игра отменена', 1]
            send_email_admin(request.form['about'], user.name, user.dt_start)

        return render_template('game_url.html', params=params)
    else:
        return 'ERROR'


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


def create_session(db_sess):
    params = {}
    params['now_date'] = dt.date.today().strftime("%d %B")
    params['week_date'] = (dt.date.today() + dt.timedelta(days=6)).strftime("%d %B")
    params['days'] = [(dt.date.today() + dt.timedelta(days=i)).strftime('%d %B %A').split() for i in range(7)]
    params['booking'] = [i[0] for i in db_sess.query(User.dt_start).all()]
    params['message'] = ['', 0]
    params['date'] = ''
    params['time'] = ''
    return params


def debug_on():
    if not application.debug:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240,
                                           backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        application.logger.addHandler(file_handler)

        application.logger.setLevel(logging.INFO)
        application.logger.info('Microblog startup')


def main():
    db_session.global_init(os.getenv('DATABASE_URL'))
    # debug_on()
    application.run(host='0.0.0.0', debug=False)


if __name__ == '__main__':
    main()