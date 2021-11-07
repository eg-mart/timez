from database.session import create_session
from database.list_table import ListTable
from task import Task
import itertools


class List:
    id_iter = itertools.count()

    def __init__(self):
        self.name = 'Новый список'
        self.tasks = []
        self.id = next(List.id_iter)

    @staticmethod
    def load_all():
        lists = []

        session = create_session()
        with session.begin():
            lists_data = session.query(ListTable).all()

        for list_data in lists_data:
            lst = List()
            lst.id = list_data.id
            lst.name = list_data.name
            lst.tasks = Task.load_list(lst.id)
            lists.append(lst)

        return lists

    def save(self):
        session = create_session()
        with session.begin():
            list_data = session.query(ListTable).filter(ListTable.id == self.id).first()
            if list_data is None:
                session.add(ListTable(id=self.id, name=self.name))
            else:
                list_data.name = self.name
