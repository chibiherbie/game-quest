import locale
import schedule
import datetime as dt
from _data import db_session
from _data.users import User

TIME = ['10:00', '11:30', '13:00', '14:30', '16:00', '17:30', '19:00']
locale.setlocale(locale.LC_ALL, "ru")  # задаем локально для вывода даты на русском


def del_time(time):
    db_sess = db_session.create_session()

    now = f'{time} {dt.date.today().strftime("%d %B %A").lower()}'
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


def del_day():
    db_sess = db_session.create_session()

    day_del = (dt.date.today() - dt.timedelta(days=1)).strftime("%d %B").lower()
    day = db_sess.query(User).filter(User.dt_start.like(f'%{day_del}%')).all()

    for i in day:
        db_sess.delete(i)
    db_sess.commit()
    print(f'День {day_del} удалён')


for i in TIME:
    schedule.every().day.at(i).do(del_time, time=i)

schedule.every().day.at('01:00').do(del_day)


while True:
    db_session.global_init("db/quest.db")
    schedule.run_pending()

