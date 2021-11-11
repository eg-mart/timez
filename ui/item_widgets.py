from PyQt5.QtWidgets import QWidget, QLabel, QToolButton, QHBoxLayout
from PyQt5.QtGui import QPixmap, QColor, QIcon


class ListItemWidget(QWidget):
    def __init__(self, lst):
        super().__init__()
        self.color_code = QLabel(self)
        pixmap = QPixmap(14, 32)
        pixmap.fill(QColor(*lst.color))
        self.color_code.setPixmap(pixmap)
        self.name = QLabel(self)
        self.name.setText(lst.name)
        self.edit = QToolButton(self)
        self.edit.setIcon(QIcon('ui/pencil.png'))

        self.all_layout = QHBoxLayout(self)
        self.all_layout.addWidget(self.color_code)
        self.all_layout.addWidget(self.name)
        self.all_layout.addWidget(self.edit)

        self.all_layout.setStretch(1, 1)
        self.all_layout.setContentsMargins(0, 5, 5, 5)

        self.list = lst

    def set_list_editor(self, edit_list_func):
        self.edit.clicked.connect(lambda: edit_list_func(self.list))


class TaskItemWidget(QWidget):
    def __init__(self, task):
        super().__init__()
        self.color_code = QLabel(self)
        colors = ["red", "yellow", "grey", "grey"]
        pixmap = QPixmap(14, 32)
        pixmap.fill(QColor(colors[task.priority - 1]))
        self.color_code.setPixmap(pixmap)
        self.name = QLabel(self)
        self.name.setText(task.name)

        self.all_layout = QHBoxLayout(self)
        self.all_layout.addWidget(self.color_code)
        self.all_layout.addWidget(self.name)

        self.all_layout.setStretch(1, 1)
        self.all_layout.setContentsMargins(0, 5, 5, 5)

        self.task = task
