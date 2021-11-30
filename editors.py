from PyQt5.QtWidgets import QWidget, QMenu, QColorDialog
from PyQt5.QtCore import QDate
from PyQt5.QtGui import QPixmap, QIcon, QColor
from PyQt5 import uic
from ui.checkable_combobox import CheckableComboBox
from ui import filter_editor, task_editor, list_editor


class TaskEditor(QWidget, task_editor.Ui_Form):
    def __init__(self, task, main_window):
        super().__init__()
        self.task = task
        self.main_window = main_window

        self.setupUi(self)
        self.name.setText(task.name)
        self.priority.setValue(task.priority)
        self.tags.setText(', '.join(task.tags))

        if task.start_date is not None:
            self.start_date.setDate(task.start_date)
            self.enable_start_date.setChecked(True)
        else:
            self.start_date.setDate(QDate.currentDate())
        if task.end_date is not None:
            self.end_date.setDate(task.end_date)
            self.enable_end_date.setChecked(True)
        else:
            self.end_date.setDate(QDate.currentDate())

        self.save.clicked.connect(self.on_save)
        self.delete_task.clicked.connect(self.on_delete)

        self.move(self.main_window.rect().center() - self.rect().center())

    def on_delete(self):
        self.task.delete()
        self.main_window.update_tasks()
        self.main_window.update_default_lists()
        self.close()

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
        self.main_window.update_default_lists()
        self.main_window.show_task(self.task)
        self.close()


class ListEditor(QWidget, list_editor.Ui_Form):
    def __init__(self, lst, main_window):
        super().__init__()
        self.list = lst
        self.main_window = main_window

        self.setupUi(self)

        self.name.setText(self.list.name)
        if self.list.start_date is not None:
            self.start_date.setDate(self.list.start_date)
            self.enable_start_date.setChecked(True)
        else:
            self.start_date.setDate(QDate.currentDate())
        if self.list.end_date is not None:
            self.end_date.setDate(self.list.end_date)
            self.enable_end_date.setChecked(True)
        else:
            self.end_date.setDate(QDate.currentDate())
        pixmap = QPixmap(32, 32)
        pixmap.fill(QColor(*self.list.color))
        self.color.setIcon(QIcon(pixmap))

        self.color.clicked.connect(self.change_color)
        self.save.clicked.connect(self.on_save)
        self.delete_list.clicked.connect(self.on_delete)

        self.move(self.main_window.rect().center() - self.rect().center())

    def change_color(self):
        color = QColorDialog.getColor(parent=self)
        if color.isValid():
            self.list.color = [int(color.redF() * 255), int(color.greenF() * 255),
                               int(color.blueF() * 255)]
            pixmap = QPixmap(32, 32)
            pixmap.fill(color)
            self.color.setIcon(QIcon(pixmap))

    def on_save(self):
        self.list.name = self.name.text()

        if self.enable_start_date.isChecked():
            self.list.start_date = self.start_date.date()
        else:
            self.list.start_date = None
        if self.enable_end_date.isChecked():
            self.list.end_date = self.end_date.date()
        else:
            self.list.end_date = None

        self.list.save()
        self.main_window.update_lists()
        self.close()

    def on_delete(self):
        self.list.delete()
        self.main_window.lists.clear()
        self.main_window.load_lists()
        self.close()


class FilterEditor(QWidget, filter_editor.Ui_Form):
    def __init__(self, lst, main_window):
        super().__init__()
        self.list = lst
        self.main_window = main_window

        self.setupUi(self)

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
        else:
            self.start_date.setDate(QDate.currentDate())
        if self.list.filtration['end_date'] is not None:
            self.enabled_end_date.setChecked(True)
            self.end_date.setDate(self.list.filtration['end_date'])
        else:
            self.end_date.setDate(QDate.currentDate())

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
