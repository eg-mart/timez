from PyQt5.QtWidgets import QWidget, QMenu
from PyQt5.QtCore import QEvent
from PyQt5 import uic
from ui.checkable_combobox import CheckableComboBox


class TaskEditor(QWidget):
    def __init__(self, task, main_window):
        super().__init__()
        self.task = task
        self.main_window = main_window

        uic.loadUi('ui/task_editor.ui', self)
        self.name.setText(task.name)
        self.priority.setValue(task.priority)
        self.tags.setText(', '.join(task.tags))

        if task.start_date is not None:
            self.start_date.setDate(task.start_date)
            self.enable_start_date.setChecked(True)
        if task.end_date is not None:
            self.end_date.setDate(task.end_date)
            self.enable_end_date.setChecked(True)

        self.save.clicked.connect(self.on_save)

        self.move(self.main_window.rect().center() - self.rect().center())

    def on_save(self):
        self.task.name = self.name.text()
        self.task.priority = int(self.priority.text())
        self.task.tags = self.tags.text().split(', ')

        if self.enable_start_date.isChecked():
            self.task.start_date = self.start_date.date()
        else:
            self.task.start_date = None
        if self.enable_end_date.isChecked():
            self.task.end_date = self.end_date.date()
        else:
            self.task.end_date = None

        self.task.save()
        self.main_window.update_tasks()
        self.close()


class ListEditor(QWidget):
    pass


class FilterEditor(QWidget):
    def __init__(self, lst, main_window):
        super().__init__()
        self.list = lst
        self.main_window = main_window

        uic.loadUi('ui/filter_editor.ui', self)
        self.priority = CheckableComboBox(self)
        items = [1, 2, 3, 4]
        for item in items:
            if item in self.list.filtration['priority']:
                self.priority.addItem(str(item), is_checked=True)
            else:
                self.priority.addItem(str(item), is_checked=False)

        self.tags = CheckableComboBox(self)
        tags = set()
        for task in self.list.tasks:
            tags.update(set(task.tags) - {''})
        for tag in tags:
            if tag in self.list.filtration['tags']:
                self.tags.addItem(tag, is_checked=True)
            else:
                self.tags.addItem(tag, is_checked=False)

        self.gridLayout.addWidget(self.priority, 0, 2)
        self.gridLayout.addWidget(self.tags, 1, 2)

        if self.list.filtration['start_date'] is not None:
            self.enabled_start_date.setChecked(True)
            self.start_date.setDate(self.list.filtration['start_date'])
        if self.list.filtration['end_date'] is not None:
            self.enabled_end_date.setChecked(True)
            self.end_date.setDate(self.list.filtration['end_date'])

        self.accept.clicked.connect(self.on_save)
        self.cancel.clicked.connect(self.close)

        self.move(self.main_window.rect().center() - self.rect().center())

    def on_save(self):
        self.list.filtration['tags'] = list(set(self.tags.getChecked()))
        self.list.filtration['priority'] = list(map(int, self.priority.getChecked()))
        if self.enabled_end_date.isChecked():
            self.list.filtration['end_date'] = self.end_date.date()
        else:
            self.list.filtration['end_date'] = None
        if self.enabled_start_date.isChecked():
            self.list.filtration['start_date'] = self.start_date.date()
        else:
            self.list.filtration['start_date'] = None
        self.list.save()
        self.main_window.update_tasks()
        self.close()
