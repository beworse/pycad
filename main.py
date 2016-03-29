#!/usr/bin/python
# -*- coding: utf-8 -*-

#----------------------------------------------------------------------#
#CELE TEGO PLIKU:
#- stworzenie GUI
#- komunikacje miedzy uzytkownikiem a pozostalymi klasami
#- nie odrysowuje w tej klasie obiektu GLWidet - to musi dziac sie wewnatrz tej klasy
#----------------------------------------------------------------------#

#podstawoe biblioteki pythona
import sys #System-specific parameters and functions
import os # Miscellaneous operating system interfaces

import string #Common string operations
import shutil #High-level file operations

import shutil #High-level file operations
import time #Time access and conversions

#biblioteka QT
from PyQt4 import QtGui, QtCore, uic
from PyQt4.QtCore import QString, Qt

#Widgety
from gui_window import Ui_MainWindow #ui glownego okna
from GLWidget import GLWidget #import GLWidget #klasa obslugujaca opengl
from Widgety import WidgetList,WidgetXY

app = QtGui.QApplication(sys.argv)
__version__ = "0.1.1" #wersja programu

class MainWindow(QtGui.QMainWindow):
	def __init__(self):#inicjalizacja klasy
		QtGui.QMainWindow.__init__(self)

	#inicjalizacji glownego ui
		ui = self.ui = Ui_MainWindow() 
		self.ui.setupUi(self)
		self.show()
		
		self.addWidgets() #dodanie pozostalych widgetow
		self.connectSignals() #polaczenie sygnalow ze slotami
		self.flags() #stworzenie/ustawinie flag
		self.variables() #inicjalizacja zmiennych
		self.setToolTipsForAll() #ustawia wskazowki do wsyzstkich narzezi
		self.setWindowTitle("PyCAD")
	
	def addWidgets(self):#dodanie widgetow do glownego okna
		#opengl
		self.qgl = GLWidget(self) 
		self.ui.horizontalLayout.addWidget(self.qgl) #dodanie widgeta zajmujacego sie obsluga opengl do glownego okna
		
		#lista obiektow
		self.widgetlist = WidgetList()
		self.ui.horizontalLayout.addWidget(self.widgetlist)
		self.widgetlist.hide()
		
		#przyciski do recznego wprowadzania danych
		self.widgetxy = WidgetXY()
		self.ui.verticalLayoutDown.addWidget(self.widgetxy)
		#self.widgetxy.hide()
	
	def flags(self): #flagi
		self.setMouseTracking(False) #wylaczenie sledzenia myszki w glownym oknie
		self.f_saved = True #czy plik zostal zapisany
		self.setAcceptDrops(True)
	
	def variables(self): #wykorzystywane zmienne
		self.markedobjects = [] #zaznaczone obiekty
		self.nrofconstobjt = 2
		self.fname = "" #nazwa pliku
		self.zoom = 0.5 #o ile bedzie zmienial sie widok
		self.dxdy = 0.5 #o ile przesuwam scene przy uzyciu strzalek
	
	def connectSignals(self):#polaczenie sygnalow i slotow
	#sygnaly wyemitowane przez qgl przypisanego do jednego slota (nie ma potrzeby rozroznienia tych zdarzen w tym miejscu)
		self.qgl.s_mousepos.connect(self.qglMouse) #zmiana pozycji
		self.qgl.s_mousepress.connect(self.qglMouse) #klikniecie 
		self.qgl.s_newobj.connect(self.addedObjWidgetList)#dodano nowy obiekt do listy
		self.qgl.s_filechanged.connect(self.FileNotSaved)
		self.qgl.s_zoomend.connect(self.zoomSignal) 
		
	#lista
		self.widgetlist.ui.pushButtonDown.clicked.connect(self.pushButtonDown)
		self.widgetlist.ui.pushButtonUp.clicked.connect(self.pushButtonUp)
		self.widgetlist.ui.pushButtonUsun.clicked.connect(self.pushButtonRemove)
		self.widgetlist.ui.listWidget.itemClicked.connect(self.clickWidgetList)
		self.widgetlist.ui.listWidget.itemSelectionChanged.connect(self.clickWidgetList)
	
	#Przyciski - niestety klasa QSignalMapper nie dziala wec zostaje to
		self.ui.pushButtonNarz0.clicked.connect(self.pushButtonNarz0)
		self.ui.pushButtonNarz1.clicked.connect(self.pushButtonNarz1)
		self.ui.pushButtonNarz2.clicked.connect(self.pushButtonNarz2)
		self.ui.pushButtonNarz3.clicked.connect(self.pushButtonNarz3)
		self.ui.pushButtonNarz4.clicked.connect(self.pushButtonNarz4)
		self.ui.pushButtonNarz5.clicked.connect(self.pushButtonNarz5)
		self.ui.pushButtonNarz6.clicked.connect(self.pushButtonNarz6)
		self.ui.pushButtonNarz7.clicked.connect(self.pushButtonNarz7)
		self.ui.pushButtonNarz8.clicked.connect(self.pushButtonNarz8)
		
	#menubar - plik
		self.ui.actionNowy.triggered.connect(self.newAction) #wcisniecie przycisku nowy
		self.ui.actionZakoncz.triggered.connect(self.closeEvent) #uwaga dwa razy wola zamkniecie
		self.ui.actionZapisz.triggered.connect(self.saveFile) #zapisanie
		self.ui.actionZapisz_jako.triggered.connect(self.saveFileAs) #zapisz jako
		self.ui.actionOtworz.triggered.connect(self.loadAction) #otwarcie pliku
		self.ui.actionZakoncz.triggered.connect(self.closeEvent) #wcisniecie przycisku nowy
		
	#menubar - edycja
		self.ui.actionCofnij.triggered.connect(self.menubarBack)
		self.qgl.s_previous.connect(self.signalMenubarBack)
		
		self.ui.actionPonow.triggered.connect(self.menubarForward) 
		self.qgl.s_next.connect(self.signalMenubarNext)
		
	#menubar - widok
		self.ui.actionPowieksz.triggered.connect(self.ZoomInView)
		self.ui.actionPomniejsz.triggered.connect(self.ZoomOutView)
		self.ui.actionStandardowy.triggered.connect(self.defaultView)
		
	def setToolTipsForAll(self): #ustawia wskazowki do wszystkich narzedzi
		#--- Ui_MainWindow (glowne ui) ---#
		self.defaultToolTipStyleForButton(self.ui.pushButtonNarz0,"Zaznaczenie jednego obiektu")
		self.defaultToolTipStyleForButton(self.ui.pushButtonNarz1,"Linia")
		self.defaultToolTipStyleForButton(self.ui.pushButtonNarz2,"Linie laczace sie")
		self.defaultToolTipStyleForButton(self.ui.pushButtonNarz3,"Tworzenie luku")
		self.defaultToolTipStyleForButton(self.ui.pushButtonNarz4,"Lista obiektow")
		self.defaultToolTipStyleForButton(self.ui.pushButtonNarz5,"Linia + kat - do wycofania") 
		self.defaultToolTipStyleForButton(self.ui.pushButtonNarz6,"Zaznaczenie wielu obiektow")
		self.defaultToolTipStyleForButton(self.ui.pushButtonNarz7,"Strzalki (nie zaimplementowane)")
		self.defaultToolTipStyleForButton(self.ui.pushButtonNarz8,"Przesuwanie punktu")
	
#------------ WIDGETLIST ------------#
	def markObjectsWidgetList(self): #zanaczenie listy obiektow
		for nr in self.markedobjects:
			self.qgl.setMarkedObj(nr)
	
	def unmarObjectsWidgetList(self):#odznaczenie listy obiektow
		for nr in self.markedobjects:
			self.qgl.setUnmarkedObj(nr)
		self.markedobjects = []
	
	def addedObjWidgetList(self): #osbluga sygnalu o dodaniu nowego obiektu do sceny
		self.widgetlist.ui.listWidget.addItem(self.qgl.obj[-1].WhatAmILongTxt())
	
	def clickWidgetList(self):#obsluga klikniecia na listWidget
	#odznaecznie obiekotw
		self.unmarObjectsWidgetList()
	#odczytanie ktory obiekt ma byc zaznaczony
		nr = self.widgetlist.ui.listWidget.currentIndex().row()
		nr = nr + self.nrofconstobjt
		self.markedobjects.append(nr)
	#zaznaczenie obiektow
		self.markObjectsWidgetList()
		
	def createWidgetList(self):#stworzenie calej listy od zera
		lengthobj = len(self.qgl.obj)
		if(lengthobj > self.nrofconstobjt): #cos wiecej niz osie X,Y
			self.widgetlist.ui.listWidget.clear()
			for i in range(self.nrofconstobjt,lengthobj):
				self.widgetlist.ui.listWidget.addItem(self.qgl.obj[i].WhatAmILongTxt()) #objekty sie przedstawia w odpowiednim formacie wystarczy je dodac do listy
				
	def pushButtonUp(self): #zmiana kolejnosci obiektow 
		if(len(self.widgetlist.ui.listWidget.selectedItems()) != 0):
		#numer wybranej linii liczony od 0
			nr = self.widgetlist.ui.listWidget.currentIndex().row() 
			if(nr != 0):
				
			#zamiana w liscie
				item = self.widgetlist.ui.listWidget.item(nr-1).text()
				self.widgetlist.ui.listWidget.item(nr-1).setText(self.widgetlist.ui.listWidget.item(nr).text())
				self.widgetlist.ui.listWidget.item(nr).setText(item)
				self.widgetlist.ui.listWidget.setCurrentItem(self.widgetlist.ui.listWidget.item(nr-1))
				
			#zmiany na obiektach
				self.unmarObjectsWidgetList()
				nr = nr + self.nrofconstobjt
				self.qgl.swapObj(nr,nr-1)
				self.markedobjects.append(nr-1)
				self.markObjectsWidgetList()
		
	def pushButtonDown(self): #zmiana kolejnosci obiektow
		if(len(self.widgetlist.ui.listWidget.selectedItems()) != 0):
			nr = self.widgetlist.ui.listWidget.currentIndex().row() #numer wybranej linii liczony od 0
			if(nr != (len(self.widgetlist.ui.listWidget)-1)):
			#zamiana w liscie
				item = self.widgetlist.ui.listWidget.item(nr+1).text()
				self.widgetlist.ui.listWidget.item(nr+1).setText(self.widgetlist.ui.listWidget.item(nr).text())
				self.widgetlist.ui.listWidget.item(nr).setText(item)
				
			#zmiany na obiektach
				self.unmarObjectsWidgetList()
				nr = nr + self.nrofconstobjt
				self.qgl.swapObj(nr,nr+1)
				self.widgetlist.ui.listWidget.setCurrentItem(self.widgetlist.ui.listWidget.item(nr+1-self.nrofconstobjt))
		
	def pushButtonRemove(self): #usuwa obiekty ze sceny
		if(len(self.widgetlist.ui.listWidget.selectedItems()) != 0):
		#odczytanie indeksu zaznaczonego obiektu na liscie
			nr = self.widgetlist.ui.listWidget.currentIndex().row() #numer wybranej linii liczony od 0
		#usuniecie numeru z listy
			item = self.widgetlist.ui.listWidget.takeItem(nr)
			del item 
		#usuniecie obiektu ze sceny
			self.qgl.removeObj(nr+self.nrofconstobjt) #usuniecie obiektu ze sceny
		#zaznaczenie kolejnego obiektu na liscie
			self.clickWidgetList() 
		#odswezenie lsity
			self.createWidgetList()
		
#------------ PRZYCISKI (TOOLS) ------------#
#tool5 - linia + kat (moze bedzie do wycofania)
#tool7 - strzalki informujace o poczatku i koncu wszystkich obiektow
#tool8 - przesuwanie pkt
	def defaultToolTipStyleForButton(self,obj,txt): #domyslny styl wskazowek dla przyciskow
		html = "<font color ='purple'><b><i>" #styl htmlowy wskaozwki - otwarcie
		html = html + txt #wlozenie stylu txt do html 
		html = html + "</i></b></font>" #styl htmlowy wskaozwki - zamkniecie
		obj.setToolTip(html) #ustawienie wskazowki wraz ze stworzonym stylem
	
	def pushButtonNarz0(self): #klikniecie na obiekt
		self.qgl.setTool(0)
	
	def pushButtonNarz1(self): #linia
		self.qgl.setTool(1)
		
	def pushButtonNarz2(self): #linia-linia
		self.qgl.setTool(2)
		
	def pushButtonNarz3(self):
		self.qgl.setTool(3)
		
	def pushButtonNarz4(self): #lista
		if(self.widgetlist.isVisible() == True):
			self.widgetlist.hide()
		else:
			self.widgetlist.show()
		self.qgl.setTool(4)
		
	def pushButtonNarz5(self):
		self.qgl.setTool(5)
	
	def pushButtonNarz6(self): #zaznaczanie wielu obiektow na scenie
		self.qgl.setTool(6)
	
	def pushButtonNarz7(self):
		self.qgl.setTool(7)
		
	def pushButtonNarz8(self):
		self.qgl.setTool(8)
	
#------------ MYSZKA ------------#
	def qglMouse(self): #wczytanie pozycji myszki na scenie i umieszczenie jej w status barze
		mousepos = self.qgl.mousepos
		mousepos = "%.4f : %.4f" % (mousepos[0], mousepos[1]) #ustawienie odpowiedniego formatu
		self.ui.statusbar.showMessage(mousepos,0) #wyswietlenie infromacji w statusbar
	
#------------ KLAWIATURA ------------#
	def keyPressEvent(self, event): #wcisniecie przycisku
		key = event.key()
		
		#-- usuwanie --#
		if(key == QtCore.Qt.Key_Delete):
			if(self.qgl.tool==0): #zaznaczony obiekt 
				self.qgl.removeObjs(self.qgl.listclicked)
				self.qgl.listclicked = []
				self.createWidgetList()
			elif(self.qgl.tool==4): #sortowanie
				self.pushButtonRemove()
		
		#-- anulowanie akacji --#
		elif(key == QtCore.Qt.Key_Escape):
			 self.qgl.cancelDraw()
			 
		#przesuwanie sceny
		elif(key == QtCore.Qt.Key_Left):
			self.qgl.changedxView(-self.dxdy)
		
		elif(key == QtCore.Qt.Key_Right):
			self.qgl.changedxView(self.dxdy)
		
		elif(key == QtCore.Qt.Key_Up):
			self.qgl.changedyView(self.dxdy)
		
		elif(key == QtCore.Qt.Key_Down):
			self.qgl.changedyView(-self.dxdy)
	
#------------ KLAWIATURA ------------#
	def FileNotSaved(self): #zmienia tytul okna gdy wystepuje taka potrzeba
		if(self.f_saved == True):
		#ustawienie tytulu okna na niezapisana
			txt = str(self.windowTitle())
			txt = "*"+txt 
			self.setWindowTitle(txt)
			self.f_saved = False 
			self.ui.actionZapisz.setEnabled(True)
	
#------------ MENUBAR  - WIDOK ------------#
	def defaultView(self): #ustawia standarowy widok
		self.ui.actionPomniejsz.setEnabled(True)
		self.ui.actionPowieksz.setEnabled(True)
		self.qgl.defaultZoomView()
	
	def zoomSignal(self,signal): #dba o to czy uzytkownik moze kliknac powieksz lub pomniejsz
		if(signal == 0):
			self.ui.actionPowieksz.setEnabled(False)
		elif(signal == 1):
			self.ui.actionPomniejsz.setEnabled(False)
			
		else:
			self.ui.actionPomniejsz.setEnabled(True)
			self.ui.actionPowieksz.setEnabled(True)
	
	def ZoomInView(self): #zmienia wielkosc sceny
		self.qgl.changeZoomView(-self.zoom)
		
	def ZoomOutView(self): #zmienia wielkosc sceny
		self.qgl.changeZoomView(self.zoom)
		
#------------ MENUBAR  - EDYCJA ------------#
	def menubarBack(self): #cofnij ctrl+z
		self.qgl.previousStepJourney()
	
	def signalMenubarBack(self,i): #zablokowuje/odblokowuje przycisk cofnij
		self.ui.actionCofnij.setEnabled(i)
		
	def signalMenubarNext(self,i): #zablokowuje/odblokowuje przycisk naprzod
		self.ui.actionPonow.setEnabled(i)
	
	def menubarForward(self): #naprzod ctrl+z+shift
		self.qgl.nextStepJourney()
	
#------------ MENUBAR  - PLIK ------------#
	#--- Nowy plik ---
	def newAction(self): #nowa scena 
		if(self.f_saved == False):
			self.doYouWantToSaveFile("Czy przed stworzeniem nowego pliku chcesz zapsiac?")
		
		self.qgl.clearMysefl()
		self.fname = ""
		self.f_saved = True
		self.setWindowTitle("PyCAD")
		self.qgl.update()

	#---Zakmniecie programu ---
	def closeEvent(self,event): #zamkniecie aplikacji - rowniez przez krzyzyk
		if(self.f_saved == False):
			self.doYouWantToSaveFile("Czy przed wyjsciem, chcesz zapisac zmiany?")
			self.f_saved = True
		self.close()
	
	#--- Zapisanie pliku ---
	def localAskDialog(self,txt): #Message box ktory pyta czy chcesz zapisac plik 
		mbox = QtGui.QMessageBox()
		
		mbox.setWindowTitle("Zapis?")
		mbox.setText(txt)
		mbox.setIcon(QtGui.QMessageBox.Warning)
		
		mbox.setStandardButtons(QtGui.QMessageBox.Yes) 
		mbox.addButton(QtGui.QMessageBox.No)
		mbox.setDefaultButton(QtGui.QMessageBox.No)
		
	#zmiana wyswietlanych napisow na przyciskach
		buttons = mbox.buttons()
		buttons[0].setText("Tak")
		buttons[1].setText("Nie")
		
		if(mbox.exec_() == QtGui.QMessageBox.Yes):
			return True
		else:
			return False
	
	def localSaveDialog(self): #dialog wywolywany do wczytania sciezki do pliku przy zapisie
		fdialog = QtGui.QFileDialog(self)
		
		#ustawienie trybu
		fdialog.setFileMode(QtGui.QFileDialog.AnyFile)
		
		#fdialog.setNameFilters(["data exchange format (*.dxf)", "downolny plik (*.*)"]) #jak dodac inne 
		fdialog.setNameFilters(["data exchange format (*.dxf)"]) #filtry do wyboru
		fdialog.selectNameFilter("data exchange format (*.dxf)") #domyslny filtr
		
		#ustawienie tekstu na polski
		fdialog.setLabelText(QtGui.QFileDialog.LookIn,"aktualny folder")
		fdialog.setLabelText(QtGui.QFileDialog.FileName,"nazwa pliku")
		fdialog.setLabelText(QtGui.QFileDialog.FileType,"rozszerzenie")
		fdialog.setLabelText(QtGui.QFileDialog.Accept,"Zapisz")
		fdialog.setLabelText(QtGui.QFileDialog.Reject,"Anuluj")
		
		#tytul oknas
		fdialog.setWindowTitle("Zapisywanie pliku")
		
		if(fdialog.exec_()):
			fname = fdialog.selectedFiles()[0]
		
		if(fdialog.result() == 1):
			
			fname = str(fname) #konwertuje na stirng pythona, bo tak wynikiem jest QString
			tmp = fname.split(".")
			
			if(tmp[-1] != "dxf"): 
				fname = fname + ".dxf"
			
			return fname
		else:
			return ""
	
	def saveFile(self): #zapisuje plik
		self.qgl.cancelDraw()
		
		if(self.fname == ""): #odczytanie sciezki do pliku
			 
			fname = self.localSaveDialog()
			
			if(fname != ""):
				self.fname = fname
		
		if(self.fname != ""):
			if(self.qgl.DXFSave(self.fname) ==  True):
				
				self.setWindowTitle(self.fname)
				self.f_saved = True
				self.ui.actionZapisz.setEnabled(False)
	
	def saveFileAs(self): #zapisz jako (korzysta z metody saveFile)
		self.qgl.cancelDraw() 
		
		fname = self.localSaveDialog()
		if(fname != ""):
			self.fname = fname
			self.saveFile()
	
	def doYouWantToSaveFile(self,txt):
		if(self.f_saved == False): #zmiany nie zapisane
			if(self.localAskDialog(txt) == True):
				if(len(self.qgl.obj) != self.qgl.howmanyignore ): #czy plik zostal wlasnie utworzony?
					self.saveFile()
	
	#--- Wczytanie pliku ---
	def localLoadDialog(self): #dialog wywolywany do wczytania sciezki do pliku przy otwieraniu pliku
		fdialog = QtGui.QFileDialog(self)
		
		#ustawienie trybu
		fdialog.setFileMode(QtGui.QFileDialog.AnyFile)
		
		#fdialog.setNameFilters(["data exchange format (*.dxf)", "downolny plik (*.*)"]) #jak dodac inne 
		fdialog.setNameFilters(["data exchange format (*.dxf)"]) #filtry do wyboru
		fdialog.selectNameFilter("data exchange format (*.dxf)") #domyslny filtr
		
		#ustawienie tekstu na polski
		fdialog.setLabelText(QtGui.QFileDialog.LookIn,"aktualny folder")
		fdialog.setLabelText(QtGui.QFileDialog.FileName,"nazwa pliku")
		fdialog.setLabelText(QtGui.QFileDialog.FileType,"rozszerzenie")
		fdialog.setLabelText(QtGui.QFileDialog.Accept,"Wczytaj")
		fdialog.setLabelText(QtGui.QFileDialog.Reject,"Anuluj")
		
		#tytul okna
		fdialog.setWindowTitle("Wczytywanie pliku")
		
		if(fdialog.exec_()):
			fname = fdialog.selectedFiles()[0]
		
		if(fdialog.result() == 1):
			fname = str(fname) #konwertuje na stirng pythona, bo tak wynikiem jest QString
			tmp = fname.split(".")
			
			if(tmp[-1] != "dxf"): #sprawdza czy znany jest format
				return ""
				
			else:
				return fname
		else:
			return ""
	
	def loadDXF(self,fname): #wczytanie pliku
		self.qgl.clearMysefl()
		result = self.qgl.DXFLoad(fname)
		
		if(result == True):
			self.fname = fname
			self.setWindowTitle(fname)
			self.f_saved = True
			QtGui.QMessageBox.information(self, 'Wczytywanie', "Plik zostal wczytany pomyslnie",QtGui.QMessageBox.Ok)
			self.createWidgetList()
			
		elif(result == False):
			self.newAction()
			QtGui.QMessageBox.information(self, 'Wczytywanie', "Wczytywanie pliku nie powiodlo sie",QtGui.QMessageBox.Ok)
	
	def loadAction(self): #wczytywanie 
		self.doYouWantToSaveFile("Czy chcesz zapisac zmiany przed otwraciem pliku")
		fname = self.localLoadDialog()
		if(fname != ""):
			self.loadDXF(fname)
	
#------------ DRAG & DROP (do wczytania) ------------#
	def loadDrop(self,fname):  #wczytanie pliku przy uzyciu drag and drop
		self.doYouWantToSaveFile("Czy chcesz zapisac zmiany przed otwraciem pliku")
		self.loadDXF(fname)
	
	def dragEnterEvent(self, event): #przesuniecie obiektu na obszar main window
		if event.mimeData().hasUrls():
			event.acceptProposedAction()
		else:
			event.ignore()
	
	def dropEvent(self, event): #po upuszczeniu obiektu zrob cos z nim
		if ( len(event.mimeData().urls()) == 1): #sprawdza czy tylko jeden plik zostal upuszczony
			url = event.mimeData().urls()[0] #konwenture liste QUrl na QUrl
			url = str(url.path()) #konwertuje Qurl na sciezke a potem na pythonoweg stringa
			tmp = url.split(".") 
			if(tmp[-1] == "dxf"): #sprawdza czy foramt to "dxf"
				self.loadDrop(url)
			else:
				event.ignore()
		else:
			event.ignore() #ignoruje drop jesli wystapi wiecej niz jeden plik
	
print "Uruchamianie PYCAD v%s..." % (__version__)
root = MainWindow()
ret = app.exec_()
