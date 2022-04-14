import datetime
import sqlalchemy
# нужно продумать связь коллекции пользователя и таблиц
# from sqlalchemy import orm

from .db_session import SqlAlchemyBase


user_to_app = sqlalchemy.Table(
    'user_to_app',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('users', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('users.id')),
    sqlalchemy.Column('apps', sqlalchemy.Integer,                      sqlalchemy.ForeignKey('apps.id'))
)


class App(SqlAlchemyBase):
    __tablename__ = 'apps'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)

    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    developer = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    publisher = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    price = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)

    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)