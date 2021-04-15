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


@app.route("/", methods=['GET', 'POST'])
def index():
    db_sess = db_session.create_session()

    params = {}
    params['now_date'] = dt.date.today().strftime("%d %B")
    params['week_date'] = (dt.date.today() + dt.timedelta(weeks=1)).strftime("%d %B")
    params['days'] = [(dt.date.today() + dt.timedelta(days=i)).strftime('%d %B %A').split() for i in range(7)]
    params['booking'] = [i[0] for i in db_sess.query(User.dt_start).all()]

    form = BookingForm()
    if form.validate_on_submit():
        # if form.password.data != form.password_again.data:
        #     return render_template('register.html', title='Регистрация',
        #                            form=form,
        #                            message="Пароли не совпадают")
        # if db_sess.query(User).filter(User.email == form.email.data).first():
        #     return render_template('register.html', title='Регистрация',
        #                            form=form,
        #                            message="Такой пользователь уже есть")
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


def main():
    db_session.global_init(os.environ.get('DATABASE_URL') + 'db/quest.db')
    port = int(os.environ.get("PORT", 5000))
    # print((dt.date.today() + dt.timedelta(weeks=1)).strftime("%d %B"))
    # app.run()
    app.run(host='0.0.0.0', port=port)


if __name__ == '__main__':
    main()