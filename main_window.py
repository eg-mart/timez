from PyQt5.QtWidgets import QMainWindow, QListWidgetItem
from PyQt5 import uic
from task_editor import TaskEditor
from list import List
from task import Task


class Item(QListWidgetItem):
    def __init__(self, name, obj):
        super().__init__(name)
        self.obj = obj


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/main.ui', self)
        self.tasks.itemActivated.connect(self.edit_task)
        self.lists.itemClicked.connect(self.change_list)
        self.load_lists()
        self.list_add.clicked.connect(self.add_list)
        self.task_add.clicked.connect(self.add_task)
        self.current_list = None

    def edit_task(self, item):
        self.form = TaskEditor(item.obj)
        self.form.show()
        item.setText(item.obj.name)
        self.tasks.repaint()

    def load_lists(self):
        self.lists.clear()
        lists = List.load_all()
        for lst in lists:
            self.lists.addItem(Item(lst.name, lst))

    def change_list(self, item):
        self.tasks.clear()
        tasks = item.obj.tasks
        self.current_list = item.obj
        for task in tasks:
            self.tasks.addItem(Item(task.name, task))

    def add_list(self):
        lst = List()
        self.lists.addItem(Item(lst.name, lst))
        lst.save()

    def add_task(self):
        task = Task(self.current_list.id)
        self.tasks.addItem(Item(task.name, task))
        self.current_list.tasks.append(task)
        task.save()
