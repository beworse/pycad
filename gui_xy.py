# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui_xy.ui'
#
# Created: Fri Mar 11 17:39:36 2016
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
        Form.resize(753, 48)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMaximumSize(QtCore.QSize(25555, 48))
        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setSizeConstraint(QtGui.QLayout.SetMinimumSize)
        self.gridLayout.setMargin(0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayoutxp = QtGui.QVBoxLayout()
        self.verticalLayoutxp.setObjectName(_fromUtf8("verticalLayoutxp"))
        self.lineEditxp = QtGui.QLineEdit(Form)
        self.lineEditxp.setEnabled(True)
        self.lineEditxp.setMinimumSize(QtCore.QSize(100, 0))
        self.lineEditxp.setMaximumSize(QtCore.QSize(100, 16777215))
        self.lineEditxp.setObjectName(_fromUtf8("lineEditxp"))
        self.verticalLayoutxp.addWidget(self.lineEditxp)
        self.horizontalLayout.addLayout(self.verticalLayoutxp)
        self.verticalLayoutyk = QtGui.QVBoxLayout()
        self.verticalLayoutyk.setObjectName(_fromUtf8("verticalLayoutyk"))
        self.lineEdityk = QtGui.QLineEdit(Form)
        self.lineEdityk.setEnabled(True)
        self.lineEdityk.setMinimumSize(QtCore.QSize(100, 0))
        self.lineEdityk.setMaximumSize(QtCore.QSize(100, 16777215))
        self.lineEdityk.setObjectName(_fromUtf8("lineEdityk"))
        self.verticalLayoutyk.addWidget(self.lineEdityk)
        self.horizontalLayout.addLayout(self.verticalLayoutyk)
        self.verticalLayoutdx = QtGui.QVBoxLayout()
        self.verticalLayoutdx.setObjectName(_fromUtf8("verticalLayoutdx"))
        self.lineEditdx = QtGui.QLineEdit(Form)
        self.lineEditdx.setEnabled(True)
        self.lineEditdx.setMinimumSize(QtCore.QSize(100, 0))
        self.lineEditdx.setMaximumSize(QtCore.QSize(100, 16777215))
        self.lineEditdx.setObjectName(_fromUtf8("lineEditdx"))
        self.verticalLayoutdx.addWidget(self.lineEditdx)
        self.horizontalLayout.addLayout(self.verticalLayoutdx)
        self.verticalLayoutdy = QtGui.QVBoxLayout()
        self.verticalLayoutdy.setObjectName(_fromUtf8("verticalLayoutdy"))
        self.lineEditdy = QtGui.QLineEdit(Form)
        self.lineEditdy.setEnabled(True)
        self.lineEditdy.setMinimumSize(QtCore.QSize(100, 0))
        self.lineEditdy.setMaximumSize(QtCore.QSize(100, 16777215))
        self.lineEditdy.setObjectName(_fromUtf8("lineEditdy"))
        self.verticalLayoutdy.addWidget(self.lineEditdy)
        self.horizontalLayout.addLayout(self.verticalLayoutdy)
        self.verticalLayoutxk = QtGui.QVBoxLayout()
        self.verticalLayoutxk.setObjectName(_fromUtf8("verticalLayoutxk"))
        self.lineEditxk = QtGui.QLineEdit(Form)
        self.lineEditxk.setEnabled(True)
        self.lineEditxk.setMinimumSize(QtCore.QSize(100, 0))
        self.lineEditxk.setMaximumSize(QtCore.QSize(100, 16777215))
        self.lineEditxk.setObjectName(_fromUtf8("lineEditxk"))
        self.verticalLayoutxk.addWidget(self.lineEditxk)
        self.horizontalLayout.addLayout(self.verticalLayoutxk)
        self.verticalLayoutyp = QtGui.QVBoxLayout()
        self.verticalLayoutyp.setObjectName(_fromUtf8("verticalLayoutyp"))
        self.lineEdityp = QtGui.QLineEdit(Form)
        self.lineEdityp.setEnabled(True)
        self.lineEdityp.setMinimumSize(QtCore.QSize(100, 0))
        self.lineEdityp.setMaximumSize(QtCore.QSize(100, 16777215))
        self.lineEdityp.setObjectName(_fromUtf8("lineEdityp"))
        self.verticalLayoutyp.addWidget(self.lineEdityp)
        self.horizontalLayout.addLayout(self.verticalLayoutyp)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.pushButtonzatwierdzobj = QtGui.QPushButton(Form)
        self.pushButtonzatwierdzobj.setObjectName(_fromUtf8("pushButtonzatwierdzobj"))
        self.gridLayout.addWidget(self.pushButtonzatwierdzobj, 0, 1, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.pushButtonzatwierdzobj.setText(_translate("Form", "OK", None))

