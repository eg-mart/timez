from database.session import create_session
from database.task_table import TaskTable
import itertools
import json
from PyQt5.QtCore import QDate


class Task:
    id_iter = itertools.count()

    def __init__(self, lst):
        self.priority = 4
        self.name = 'New task'
        self.end_date = None
        self.start_date = None
        self.id = next(Task.id_iter)
        self.tags = []
        self.list = lst

    @staticmethod
    def load_list(lst):
        tasks = []

        list_id = lst.id

        session = create_session()
        with session.begin():
            tasks_data = session.query(TaskTable).filter(TaskTable.list == list_id).all()

        for task_data in tasks_data:
            task = Task(0)

            if task_data.start_date != '':
                start = QDate(*json.loads(task_data.start_date))
                task.start_date = start
            else:
                task.start_date = None

            if task_data.end_date != '':
                end = QDate(*json.loads(task_data.end_date))
                task.end_date = end
            else:
                task.end_date = None

            task.name = task_data.name
            task.priority = task_data.priority
            task.tags = json.loads(task_data.tags)
            task.id = task_data.id
            task.list = lst
            tasks.append(task)

        return tasks

    def delete(self):
        session = create_session()
        with session.begin():
            session.query(TaskTable).filter(TaskTable.id == self.id).delete()
            self.list.tasks.remove(self)
            del self

    def save(self):
        session = create_session()

        if self.start_date is not None:
            start = json.dumps([self.start_date.year(), self.start_date.month(), self.start_date.day()])
        else:
            start = ''

        if self.end_date is not None:
            end = json.dumps([self.end_date.year(), self.end_date.month(), self.end_date.day()])
        else:
            end = ''

        tags = json.dumps(self.tags)

        with session.begin():
            task_data = session.query(TaskTable).filter(TaskTable.id == self.id).first()
            if task_data is None:
                session.add(TaskTable(id=self.id, name=self.name, priority=self.priority, list=self.list.id,
                                      start_date=start, end_date=end, tags=tags))
            else:
                task_data.name = self.name
                task_data.priority = self.priority
                task_data.start_date = start
                task_data.end_date = end
                task_data.tags = tags
                task_data.list = self.list.id
