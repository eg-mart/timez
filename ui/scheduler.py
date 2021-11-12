from PyQt5.QtWidgets import QCalendarWidget
from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QColor


class Scheduler(QCalendarWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.list = None
        self.main_window = None
        self.colors = ['red', 'yellow', 'green', 'grey']
        self.clicked.connect(self.on_click)

    def set_list(self, lst):
        self.list = lst

    def set_main_window(self, main_window):
        self.main_window = main_window

    def update_calendar(self):
        self.repaint()

    def on_click(self, date):
        self.list.filtration['end_date'] = date
        self.main_window.update_tasks()

    def paintCell(self, painter, rect, date):
        super().paintCell(painter, rect, date)
        for task in self.list.tasks:
            if task.end_date == date and self.colors[task.priority - 1]:
                painter.setPen(QColor(self.colors[task.priority - 1]))
                painter.setBrush(QColor(self.colors[task.priority - 1]))
                painter.drawEllipse(rect.topLeft() + QPoint(12 + (task.priority - 1) * 5, 7), 3, 3)
