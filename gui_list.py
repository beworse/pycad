# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui_list.ui'
#
# Created: Tue Mar  1 19:09:51 2016
#      by: PyQt4 UI code generator 4.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.setEnabled(True)
        Form.resize(275, 498)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setSizeConstraint(QtGui.QLayout.SetMaximumSize)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setContentsMargins(0, 0, 0, -1)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.listWidget = QtGui.QListWidget(Form)
        self.listWidget.setMinimumSize(QtCore.QSize(275, 0))
        self.listWidget.setMaximumSize(QtCore.QSize(275, 16777215))
        self.listWidget.setObjectName(_fromUtf8("listWidget"))
        self.gridLayout.addWidget(self.listWidget, 0, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.pushButtonUp = QtGui.QPushButton(Form)
        self.pushButtonUp.setMinimumSize(QtCore.QSize(87, 27))
        self.pushButtonUp.setObjectName(_fromUtf8("pushButtonUp"))
        self.horizontalLayout.addWidget(self.pushButtonUp)
        self.pushButtonDown = QtGui.QPushButton(Form)
        self.pushButtonDown.setMinimumSize(QtCore.QSize(87, 27))
        self.pushButtonDown.setObjectName(_fromUtf8("pushButtonDown"))
        self.horizontalLayout.addWidget(self.pushButtonDown)
        self.pushButtonUsun = QtGui.QPushButton(Form)
        self.pushButtonUsun.setMinimumSize(QtCore.QSize(87, 27))
        self.pushButtonUsun.setObjectName(_fromUtf8("pushButtonUsun"))
        self.horizontalLayout.addWidget(self.pushButtonUsun)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.pushButtonUp.setText(_translate("Form", "UP", None))
        self.pushButtonDown.setText(_translate("Form", "DOWN", None))
        self.pushButtonUsun.setText(_translate("Form", "Usun", None))

