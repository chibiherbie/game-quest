import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String, index=True, unique=False, nullable=True)
    address = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    dt_start = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    url = sqlalchemy.Column(sqlalchemy.String)