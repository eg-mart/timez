from PyQt5.QtWidgets import QWidget
from PyQt5 import uic


class TaskEditor(QWidget):
    def __init__(self, task):
        super().__init__()
        self.task = task
        uic.loadUi('ui/task_editor.ui', self)
        self.name.setText(task.name)
        self.priority.setValue(task.priority)
        self.start_date.setText(task.start_date)
        self.end_date.setText(task.end_date)
        self.save.clicked.connect(self.on_save)

    def on_save(self):
        self.task.name = self.name.text()
        self.task.priority = int(self.priority.text())
        self.task.start_date = self.start_date.text()
        self.task.end_date = self.end_date.text()
        self.task.save()
        self.close()
