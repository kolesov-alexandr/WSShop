import sqlalchemy

from sqlalchemy import orm
from data.db_session import SqlAlchemyBase


class Comment(SqlAlchemyBase):
    __tablename__ = 'comments'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)

    author = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))

    user = orm.relation('User')

    app_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("apps.id"))

    app = orm.relation('App')

    comment = sqlalchemy.Column(sqlalchemy.String, nullable=False)

