from PyQt5.QtWidgets import QMainWindow, QListWidgetItem, QInputDialog
from PyQt5 import uic
from PyQt5.QtCore import Qt
from editors import TaskEditor, ListEditor, FilterEditor
from list import List
from task import Task
from ui.item_widgets import ListItemWidget, TaskItemWidget


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/main.ui', self)
        self.load_lists()

        self.list_add.clicked.connect(self.add_list)
        self.task_add.clicked.connect(self.add_task)
        self.set_sort.clicked.connect(self.change_sort)
        self.set_filtration.clicked.connect(self.change_filtration)

        self.tasks.itemActivated.connect(lambda item: self.edit_task(self.tasks.itemWidget(item).task))
        self.lists.itemClicked.connect(self.change_list)

        self.current_list = None
        self.form = None

    def edit_task(self, task):
        self.form = TaskEditor(task, self)
        self.form.show()

    def edit_list(self, lst):
        self.form = ListEditor(lst, self)
        self.form.show()

    def load_lists(self):
        self.lists.clear()
        lists = List.load_all()
        for lst in lists:
            item = QListWidgetItem()
            widget = ListItemWidget(lst)
            item.setSizeHint(widget.sizeHint())
            self.lists.addItem(item, )
            self.lists.setItemWidget(item, widget)

    def change_list(self, item):
        self.current_list = self.lists.itemWidget(item).list
        self.update_tasks()

    def update_tasks(self):
        self.tasks.clear()
        tasks = self.current_list.get_tasks()
        for task in tasks:
            item = QListWidgetItem()
            widget = TaskItemWidget(task)
            item.setSizeHint(widget.sizeHint())
            self.tasks.addItem(item)
            self.tasks.setItemWidget(item, widget)

    def add_list(self):
        lst = List()
        item = QListWidgetItem()
        widget = ListItemWidget(lst)
        item.setSizeHint(widget.sizeHint())
        self.lists.addItem(item)
        self.lists.setItemWidget(item, widget)
        lst.save()

    def add_task(self):
        task = Task(self.current_list.id)
        item = QListWidgetItem()
        widget = TaskItemWidget(task)
        item.setSizeHint(widget.sizeHint())
        self.tasks.addItem(item, )
        self.tasks.setItemWidget(item, widget)
        self.current_list.tasks.append(task)
        task.save()
        self.edit_task(task)

    def change_sort(self):
        variants = ("Имени", "Дате начала", "Дате окончания", "Приоритету")
        sort, ok_pressed = QInputDialog.getItem(
            self, "Изменить сортировку", "Сортировать по...",
            variants, self.current_list.sort.value - 1, False)
        if ok_pressed:
            self.current_list.sort = List.Sort(variants.index(sort) + 1)
            self.current_list.save()
            self.update_tasks()

    def change_filtration(self):
        self.form = FilterEditor(self.current_list, self)
        self.form.show()
