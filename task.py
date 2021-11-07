from database.session import create_session
from database.task_table import TaskTable
import itertools


class Task:
    id_iter = itertools.count()

    def __init__(self, lst):
        self.priority = 0
        self.name = 'New task'
        self.end_date = None
        self.start_date = None
        self.id = next(Task.id_iter)
        self.list = lst

    @staticmethod
    def load_list(list_id):
        tasks = []

        session = create_session()
        with session.begin():
            tasks_data = session.query(TaskTable).filter(TaskTable.list == list_id).all()

        for task_data in tasks_data:
            task = Task(0)
            task.name = task_data.name
            task.priority = task_data.priority
            task.end_date = task_data.end_date
            task.start_date = task_data.start_date
            task.id = task_data.id
            task.list = task_data.list
            tasks.append(task)

        return tasks

    def save(self):
        session = create_session()
        with session.begin():
            task_data = session.query(TaskTable).filter(TaskTable.id == self.id).first()
            if task_data is None:
                session.add(TaskTable(id=self.id, name=self.name, priority=self.priority, list=self.list,
                                      start_date=self.start_date, end_date=self.end_date))
            else:
                task_data.name = self.name
                task_data.priority = self.priority
                task_data.start_date = self.start_date
                task_data.end_date = self.end_date
                task_data.list = self.list

    def on_click(self):
        pass
