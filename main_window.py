from PyQt5.QtWidgets import QMainWindow, QListWidgetItem, QInputDialog
from PyQt5 import uic
from PyQt5.QtGui import QTextCharFormat, QBrush, QColor
from PyQt5.QtCore import Qt, QDate
from editors import TaskEditor, ListEditor, FilterEditor
from list import List
from task import Task
from ui.item_widgets import ListItemWidget, TaskItemWidget
from enum import Enum
from ui.main import Ui_MainWindow


class Main(QMainWindow, Ui_MainWindow):
    View = Enum('View', 'task calendar')

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.load_lists()

        self.list_add.clicked.connect(self.add_list)
        self.task_add.clicked.connect(self.add_task)
        self.set_sort.clicked.connect(self.change_sort)
        self.set_filtration.clicked.connect(self.change_filtration)
        self.set_view.clicked.connect(self.change_view)

        self.tasks.itemActivated.connect(lambda item: self.edit_task(self.tasks.itemWidget(item).task))
        self.tasks.itemClicked.connect(lambda item: self.show_task(self.tasks.itemWidget(item).task))
        self.lists.itemClicked.connect(self.change_list)

        self.current_list = self.today_list
        self.current_view = Main.View.task
        self.form = None
        self.calendar.set_list(self.today_list)
        self.calendar.set_main_window(self)

    def edit_task(self, task):
        self.form = TaskEditor(task, self)
        self.form.show()

    def update_default_lists(self):
        for i in range(self.lists.model().rowCount()):
            for task in self.lists.itemWidget(self.lists.item(i)).list.tasks:
                if task not in self.all_list.tasks:
                    self.all_list.tasks.append(task)

        for task in self.all_list.tasks:
            if task.end_date == QDate.currentDate() or task.start_date == QDate.currentDate():
                if task not in self.today_list.tasks:
                    self.today_list.tasks.append(task)

        self.update_lists()

    def edit_list(self, lst):
        self.form = ListEditor(lst, self)
        self.form.show()

    def update_lists(self):
        lists = []
        for i in range(self.lists.model().rowCount()):
            lists.append(self.lists.itemWidget(self.lists.item(i)).list)
        self.lists.clear()
        for lst in lists:
            item = QListWidgetItem()
            widget = ListItemWidget(lst)
            widget.set_list_editor(self.edit_list)
            item.setSizeHint(widget.sizeHint())
            self.lists.addItem(item)
            self.lists.setItemWidget(item, widget)

    def load_lists(self):
        self.lists.clear()
        lists = List.load_all()
        for lst in lists:
            if lst.name in ['Все', 'Сегодня']:
                continue
            item = QListWidgetItem()
            widget = ListItemWidget(lst)
            widget.set_list_editor(self.edit_list)
            item.setSizeHint(widget.sizeHint())
            self.lists.addItem(item, )
            self.lists.setItemWidget(item, widget)

        self.all_list = List()
        self.all_list.name = 'Все'
        item = QListWidgetItem()
        widget = ListItemWidget(self.all_list)
        widget.set_list_editor(self.edit_list)
        item.setSizeHint(widget.sizeHint())
        self.lists.addItem(item)
        self.lists.setItemWidget(item, widget)
        self.today_list = List()
        self.today_list.name = 'Сегодня'
        item = QListWidgetItem()
        widget = ListItemWidget(self.today_list)
        widget.set_list_editor(self.edit_list)
        item.setSizeHint(widget.sizeHint())
        self.lists.addItem(item)
        self.lists.setItemWidget(item, widget)
        item.setSelected(True)
        self.update_default_lists()

    def change_list(self, item):
        self.current_list = self.lists.itemWidget(item).list
        self.calendar.set_list(self.current_list)
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
        self.calendar.update_calendar()

    def add_list(self):
        lst = List()
        item = QListWidgetItem()
        widget = ListItemWidget(lst)
        widget.set_list_editor(self.edit_list)
        item.setSizeHint(widget.sizeHint())
        self.lists.addItem(item)
        self.lists.setItemWidget(item, widget)
        self.edit_list(lst)
        lst.save()

    def add_task(self):
        task = Task(self.current_list)
        item = QListWidgetItem()
        widget = TaskItemWidget(task)
        item.setSizeHint(widget.sizeHint())
        self.tasks.addItem(item, )
        self.tasks.setItemWidget(item, widget)
        self.current_list.tasks.append(task)
        task.save()
        self.update_default_lists()
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

    def change_view(self):
        if self.current_view == Main.View.task:
            self.calendar.show()
            self.current_view = Main.View.calendar
        else:
            self.calendar.hide()
            self.current_view = Main.View.task

    def show_task(self, task):
        self.name.setText(task.name)
        self.priority.setText(str(task.priority))
        if task.end_date is not None:
            self.end_date.setText(task.end_date.toString())
        else:
            self.end_date.setText('-')
        if task.start_date is not None:
            self.start_date.setText(task.start_date.toString())
        else:
            self.start_date.setText('-')
        self.tags.setText(', '.join(task.tags))
