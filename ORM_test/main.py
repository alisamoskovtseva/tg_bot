import datetime

from flask import Flask
from data import db_session
from data.users import User
from sqlalchemy import orm

app = Flask(__name__)

# ПОДКЛЮЧЕНИЕ К БОТУ
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/Users.db")
    db_sess = db_session.create_session()
    # app.run()

    # ЗАНЕСЕНИЕ ДАННЫХ В ТАБЛИЦУ
    user = User()
    user.name = "Alisa lox"
    user.tg_id = '4684648'
    db_sess = db_session.create_session()
    db_sess.add(user)
    db_sess.commit()

    # ВЫВОД ДАННЫХ
    # db_sess = db_session.create_session()
    # user = db_sess.query(User).first()
    # print(user.name)

    # ТОЖЕ ВЫВОД, НО КРАСИВЫЙ(НЕ ОЧЕНЬ)
    # db_sess = db_session.create_session()
    # for user in db_sess.query(User).all():
    #     print(user)

    # ФИЛЬТРАЦИЯ
    # db_sess = db_session.create_session()
    # for user in db_sess.query(User).filter(User.id > 1, User.email.notilike("%1%")):
    #     print(user)

    # ИЗМЕНЕНИЕ ДАННЫХ
    # user = db_sess.query(User).filter(User.id == 1).first()
    # print(user)
    # user.name ="АААААА"
    # user.created_date = datetime.datetime.now()
    # db_sess.commit()

    # УДАЛЕНИЕ
    # user = db_sess.query(User).filter(User.id == 2).first()
    # db_sess.delete(user)
    # db_sess.commit()


if __name__ == '__main__':
    main()
