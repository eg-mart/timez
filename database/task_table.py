import sqlalchemy
from .session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class TaskTable(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'task'
    id = sqlalchemy.Column(sqlalchemy.INT, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    priority = sqlalchemy.Column(sqlalchemy.INT, nullable=True)
    start_date = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    end_date = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    list = sqlalchemy.Column(sqlalchemy.INT, nullable=True)
