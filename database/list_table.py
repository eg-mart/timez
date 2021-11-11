import sqlalchemy
from .session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class ListTable(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'list'
    id = sqlalchemy.Column(sqlalchemy.INT, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    color = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    sort = sqlalchemy.Column(sqlalchemy.INT, nullable=True)
    filtration = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
