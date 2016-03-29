#!/usr/bin/python
# -*- coding: utf-8 -*-

#----------------------------------------------------------------------#
#CELE TEGO PLIKU:
#- klasy ui przerabiane sa na widgety, ktore pozniej moga byc 
#wykorzystane w glownej klasie
#- chowanie niektorych obiektow
#----------------------------------------------------------------------#

#ui
from gui_list import Ui_Form as glist
from gui_xy import Ui_Form as gxy

#biblioteka QT
from PyQt4 import QtGui, QtCore, uic
from PyQt4.QtCore import QString, Qt

#klasa sluzaca do porzadkowania obietkow pomaga w tym lista
class WidgetList(QtGui.QWidget): 
	def __init__(self):
		QtGui.QMainWindow.__init__(self)
		ui = self.ui = glist() 
		self.ui.setupUi(self)
		
#klasa sluzaca do recznego wprowadznaia pkt
class WidgetXY(QtGui.QWidget):
	def __init__(self):
		QtGui.QMainWindow.__init__(self)
		ui = self.ui = gxy() 
		self.ui.setupUi(self)
		self.defaultText()
	
	def defaultText(self):
		self.ui.lineEditxp.setText("x poczatkowe")
		self.ui.lineEdityp.setText("y poczatkowe")
		self.ui.lineEditxk.setText("x koncowe")
		self.ui.lineEdityk.setText("y koncowe")
		
	def setxpyp(self,x,y):
		self.ui.lineEditxp.setText(str(x))
		self.ui.lineEdityp.setText(str(y))
		
	def setxkyk(self,x,y):
		self.ui.lineEditxp.setText(str(x))
		self.ui.lineEdityp.setText(str(y))
	
	def hidedxdy(self,co): #chowa niektore przycski
		if(co == False):
			self.ui.lineEditdxo.hide()
			self.ui.lineEditdx.hide()
			self.ui.lineEditdyo.hide()
			self.ui.lineEditdy.hide()
		else:
			self.ui.lineEditdxo.show()
			self.ui.lineEditdx.show()
			self.ui.lineEditdyo.show()
			self.ui.lineEditdy.show()
