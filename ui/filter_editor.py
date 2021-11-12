# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'filter_editor.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(340, 205)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setStyleSheet("* { background-color:rgb(41, 53, 59);  color: white;}\n"
"QPushButton {\n"
"border: 0px solid rgb(30, 39, 43);\n"
" border-right-width: 2px;\n"
"border-bottom-width: 2px;\n"
"border-top: 1px solid rgb(34, 44, 49);\n"
"border-left: 1px solid rgb(34, 44, 49);\n"
"}\n"
"QPushButton:hover {\n"
"border: 0px solid rgb(30, 39, 43);\n"
" border-right-width: 3px;\n"
"border-bottom-width: 3px;\n"
"border-top: 2px solid rgb(34, 44, 49);\n"
"border-left: 2px solid rgb(34, 44, 49);\n"
"}\n"
"QPushButton:pressed {\n"
"background-color: rgb(34, 44, 49);\n"
"}\n"
"QLabel {\n"
"    background-color: rgba(255, 255, 255, 0);\n"
"}\n"
"")
        self.gridLayoutWidget = QtWidgets.QWidget(Form)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 10, 318, 131))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.start_date = QtWidgets.QDateEdit(self.gridLayoutWidget)
        self.start_date.setCalendarPopup(True)
        self.start_date.setObjectName("start_date")
        self.gridLayout.addWidget(self.start_date, 2, 2, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 1, 1, 1)
        self.end_date = QtWidgets.QDateEdit(self.gridLayoutWidget)
        self.end_date.setCalendarPopup(True)
        self.end_date.setObjectName("end_date")
        self.gridLayout.addWidget(self.end_date, 3, 2, 1, 1)
        self.enabled_start_date = QtWidgets.QCheckBox(self.gridLayoutWidget)
        self.enabled_start_date.setText("")
        self.enabled_start_date.setObjectName("enabled_start_date")
        self.gridLayout.addWidget(self.enabled_start_date, 2, 0, 1, 1)
        self.enabled_end_date = QtWidgets.QCheckBox(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.enabled_end_date.sizePolicy().hasHeightForWidth())
        self.enabled_end_date.setSizePolicy(sizePolicy)
        self.enabled_end_date.setText("")
        self.enabled_end_date.setObjectName("enabled_end_date")
        self.gridLayout.addWidget(self.enabled_end_date, 3, 0, 1, 1)
        self.horizontalLayoutWidget = QtWidgets.QWidget(Form)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(80, 150, 170, 51))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.accept = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.accept.setMinimumSize(QtCore.QSize(0, 30))
        self.accept.setObjectName("accept")
        self.horizontalLayout.addWidget(self.accept)
        self.cancel = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.cancel.setMinimumSize(QtCore.QSize(0, 30))
        self.cancel.setObjectName("cancel")
        self.horizontalLayout.addWidget(self.cancel)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Фильтровать по..."))
        self.label_4.setText(_translate("Form", "Дате окончания:"))
        self.label.setText(_translate("Form", "Приоритету:"))
        self.label_2.setText(_translate("Form", "Тегам:"))
        self.label_3.setText(_translate("Form", "Дате начала:"))
        self.accept.setText(_translate("Form", "OK"))
        self.cancel.setText(_translate("Form", "Cancel"))
