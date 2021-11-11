from PyQt5.QtWidgets import QComboBox
from PyQt5.QtGui import QStandardItem
from PyQt5.QtCore import Qt


class CheckableComboBox(QComboBox):
    def __init__(self, parent):
        super().__init__(parent)
        self.setEditable(True)
        self.lineEdit().setReadOnly(True)
        self.model().dataChanged.connect(self.updateText)

    def addItem(self, text, is_checked=False, **kwargs):
        item = QStandardItem(text)
        item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsUserCheckable)
        if not is_checked:
            item.setData(Qt.Unchecked, Qt.CheckStateRole)
        else:
            item.setData(Qt.Checked, Qt.CheckStateRole)
        self.model().appendRow(item)
        self.updateText()

    def addItems(self, texts):
        for e in texts:
            self.addItem(e)

    def updateText(self):
        text = ", ".join(self.getChecked())
        self.lineEdit().setText(text)

    def getChecked(self):
        items = []
        for i in range(self.model().rowCount()):
            if self.model().item(i).checkState() == Qt.Checked:
                items.append(self.model().item(i).text())
        return items
