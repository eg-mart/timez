from database.session import create_session
from database.list_table import ListTable
from task import Task
import itertools
from enum import Enum
import json
from PyQt5.QtCore import QDate


class List:
    id_iter = itertools.count()
    Sort = Enum('Sort', 'name start_date end_date priority')

    def __init__(self):
        self.name = 'Новый список'
        self.color = (255, 255, 255)
        self.filtration = {'tags': [], 'end_date': None, 'start_date': None, 'priority': []}
        self.sort = List.Sort.priority
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
            lst.color = json.loads(list_data.color)
            lst.sort = List.Sort(list_data.sort)
            lst.tasks = Task.load_list(lst.id)

            filtration = json.loads(list_data.filtration)
            if filtration['start_date'] is not None:
                filtration['start_date'] = QDate(*filtration['start_date'])
            if filtration['end_date'] is not None:
                filtration['end_date'] = QDate(*filtration['end_date'])
            lst.filtration = filtration

            lists.append(lst)

        return lists

    def save(self):
        session = create_session()
        with session.begin():
            list_data = session.query(ListTable).filter(ListTable.id == self.id).first()
            color = json.dumps(self.color)

            filtration = self.filtration.copy()
            if self.filtration['start_date'] is not None:
                start = [self.filtration['start_date'].year(), self.filtration['start_date'].month(),
                         self.filtration['start_date'].day()]
            else:
                start = None

            if self.filtration['end_date'] is not None:
                end = [self.filtration['end_date'].year(), self.filtration['end_date'].month(),
                       self.filtration['end_date'].day()]
            else:
                end = None

            filtration['start_date'] = start
            filtration['end_date'] = end
            filtration = json.dumps(filtration)

            if list_data is None:
                session.add(ListTable(id=self.id, name=self.name, color=color,
                                      sort=self.sort.value, filtration=filtration))
            else:
                list_data.name = self.name
                list_data.color = color
                list_data.sort = self.sort.value
                list_data.filtration = filtration

    def get_tasks(self):
        ready_tasks = []

        for task in self.tasks:
            if (not self.filtration['tags'] or any(i in task.tags for i in self.filtration['tags'])) and\
                    (self.filtration['start_date'] is None or task.start_date == self.filtration['start_date']) and\
                    (self.filtration['end_date'] is None or task.start_date == self.filtration['end_date']) and \
                    (not self.filtration['priority'] or task.priority in self.filtration['priority']):
                ready_tasks.append(task)

        if self.sort == List.Sort.name:
            ready_tasks.sort(key=lambda x: x.name)
        elif self.sort == List.Sort.end_date:
            ready_tasks.sort(key=lambda x: x.end_date)
        elif self.sort == List.Sort.start_date:
            ready_tasks.sort(key=lambda x: x.start_date)
        elif self.sort == List.Sort.priority:
            ready_tasks.sort(key=lambda x: x.priority)

        return ready_tasks
