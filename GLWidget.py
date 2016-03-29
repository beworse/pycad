#!/usr/bin/python
# -*- coding: utf-8 -*-

#----------------------------------------------------------------------#
#CELE TEGO PLIKU:
#- obsluga myszki oraz klawiatury na opengl
#- rysowanie lini,lukow na opengl
#- modyfikacja sceny
#----------------------------------------------------------------------#

#podstawoe biblioteki pythona
import sys #System-specific parameters and functions
import os # Miscellaneous operating system interfaces

import string #Common string operations
#import re #Regular expression operations

import shutil #High-level file operations
#import time #Time access and conversions

from math import * #Mathematical functions
from datetime import datetime

#biblioteka QT
from PyQt4 import QtGui, QtCore, uic, QtOpenGL
from PyQt4.QtCore import QString, Qt

#from numpy import matrix #macierze

#biblioteki rysujace
from draw import LocalLine #zwykla prosta
from draw import SelectRect #prostokat zaznaczajacy
from draw import NearestPointRect #prostokat powstajacy przy najblizszym pkt
from draw import LocalArc #luki
from draw import LocalArrows #strzalki
#biblioteka opengl
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

class GLWidget(QtOpenGL.QGLWidget):
#------------ SYGNALY ------------#
	s_mousepos = QtCore.pyqtSignal() #zmienila sie pozycja myszki
	s_mousepress = QtCore.pyqtSignal() #przycisk myszki zostal wcisniety
	s_newobj = QtCore.pyqtSignal() #dodano nowy obiekt
	s_previous = QtCore.pyqtSignal(bool) #mozna lub nie mozna kliknac cofnij
	s_next = QtCore.pyqtSignal(bool) #mozna lub nie mozna kliknac ponow
	s_filechanged = QtCore.pyqtSignal() #zawartosc pliku sie zmienila
	s_zoomend = QtCore.pyqtSignal(int)
	#s_out = QtCore.pyqtSignal() #wyjechano po za zalozony obszar
	
#------------ INCJALIZCJA ------------#
	def __init__(self, parent):
		super(GLWidget, self).__init__(parent)
		
	#minimalny rozmiar;
		self.setMinimumWidth(300)
		self.setMinimumHeight(300)
		
	#flagi
		self.flags()
		
	#opengl
		glEnable(GL_DEPTH)
		
	#zmienne
		self.variables()
	
	def clearMysefl(self):
		self.variables()
		self.flags()
	
	def flags(self): #wszystkie flagi tworzone/ustawiane sa tutaj
		#qt
		self.setMouseTracking(True) #bez ustawienia tej flagi myszka nie bedzie sledzona
		
		#obszar roboczy
		self.f_outn = False #czu obiekt jest rysowany w zalozonym mraginesie
		self.f_outs = False #czu obiekt jest rysowany na stole
		self.f_out = False #czy zostal wyznaczony obszar roboczy (margines + stol)
		
		#najblizszy pkt
		self.f_point = False #czy znajdowac najblizszy pkt
		
		#myszka
		self.f_click = False #czy znane znane jest polozenie pierwszego klikniecia 
		self.f_mtrace = False #czy myszka myszka jest sledzona
		self.f_catch = False #czy w polizu znajduje sie punkt
		
		#scena
		self.f_update = False #czy aktualizowac scene
		self.f_text = False #czy rysowac txt
		self.f_arrows = False #czy rysowac strzalki
	
	def variables(self):#wszystkie zmienne tworozne sa tutaj
		#myszka
		self.mousepos = [] #ostatnia pozycja myszki po kliknieciu, przesunieciu
		self.mouselastclick = [] #ostatnia pozycja myszki w momencie klikniecia
		
		#narzedzia
		self.tool = 0 #wybrane narzedzie
		
		#najblizszy pkt
		self.nearestrect = NearestPointRect(0,0,0.1) 
		
		#scena
		self.minview = 0.5 #minalmny rozmiar sceny
		self.maxview = 5 #maksymalny rozmiar sceny
		self.defaultview = 2.0 #domyslny rozmiar sceny
		
		self.scenesize = [self.defaultview,0.0 , 0.0] #rozmiar sceny,przesuniecie x, przesuniecie y
		self.currentview = [0.0 , 2.0 , 0.0 , 2.0] #aktualnie wyswietlany fragment
		
		#rysowanie
		self.obj = [] #wszystkie obiekty sceny
		self.arrows = [] 
		self.mindistance = 0.01 #dopuszcalna odleglosc aby mozliwe bylo zlapanie pkt
		self.minclickdistance = 0.01 #tolerancja myszki
		self.listclicked = [] #lista kliknietych obiektow
		self.indexcatch = 0 #indeks zlapanego pkt
		
		#kronika
		self.journey = [] 
		self.journeycurrent = -1
		
		#dodanie osi X,Y
		self.addLineXY(0,0,0,2)
		self.addLineXY(0,0,2,0)
		self.howmanyignore = 2 #ile obiektow sceny nalezy ignorowac
	
#------------ FUNKCJE WYMAGANE W KLASIE QGLWidget ------------#
	def initializeGL(self): #zaladowanie moduly do pamieci
	#ustawienie kamery na 1 cwiartke
		#glRotatef(0, 1.0, 0.0, 0.0) #kat wzgledem x
		#glRotatef(0, 0.0, 1.0, 0.0) #kat wzgledem y
		#glTranslatef(-1,-1, 0)
		#gluOrtho2D(self.currentview[0],self.currentview[1],self.currentview[2], self.currentview[3])
		glutInit() #potrzebne do rysowania tekstu
		glClearColor(1.0,1.0,1.0,.0) #kolor tla
	
	def paintGL(self): #tworzy scene i ja odrysowuje
		glLoadIdentity()
		gluOrtho2D(self.currentview[0],self.currentview[1],self.currentview[2], self.currentview[3])
		glClear(GL_COLOR_BUFFER_BIT) #wyczyszczenie bufora
		self.draw() #rysuje wszystkie obiekty sceny
		glFlush() #wymuszenie rysowania
	 
	def resizeGL(self, width, height): #przeskalowuje scene bez zmiany wielkosci okna
		self.width, self.height = width, height 
		glViewport(0, 0, width, height)
	
#------------ MYSZKA ------------#
	def mouseGlboalToScenePos(self,event): #pozycja myszki na widgecie -> pozycja myszki na scenie
		mousepos = event.pos() #odczytanie pozycji myszki na widget
		
	#kowersja pozycji myszki z widgetu do pozycji na scenie
		x = float(mousepos.x()) / self.width * self.scenesize[0]
		x = x + self.scenesize[1] #dodanie przesunieca
		
		y = float(mousepos.y()) / self.height * self.scenesize[0] 
		y = -(y-self.scenesize[0]) #os y jest w opengl do gory ujemna
		y = y + self.scenesize[2] #dodanie przesuniecia
		
		self.mousepos = [x,y]
	
	def mousePressEvent(self,event): #wcisniecie myszki ale nie zwolnienie!!
		if (event.button() == QtCore.Qt.LeftButton): #sprawdzenie czy zostal wcisniety lewy przycisk myszy
			self.mouseGlboalToScenePos(event)
			self.s_mousepress.emit() #wyemitowanie sygnalu informujacego o wcisnieciu przycisku
			
			if(self.f_point==True):
				self.nearestPoint(self.mousepos[0],self.mousepos[1])
				
			if(self.tool == 0): #klikniecie na obiekt
				self.mouselastclick = self.mousepos
				self.mouselastclick.append(self.mousepos[0])
				self.mouselastclick.append(self.mousepos[1])
				self.Tool0MousePress()
				
			elif(self.tool == 1): #rysowanie linii
				self.Tool1MouseClick() 
			
			elif(self.tool == 2): #wiele lini
				self.Tool2MouseClick() 
				
			elif(self.tool == 3): #luk
				self.Tool3MouseClick() 
				
			elif(self.tool == 6): #zaznaczenie wielu obiektow
				self.Tool6MouseClick()
			
			elif(self.tool == 8): #lapanie punktow
				self.Tool8MouseClick()
	
	def mouseReleaseEvent(self,event): #zwolnienie przycisku
		if (event.button() == QtCore.Qt.LeftButton):
			if(self.tool == 0):
				if(len(self.listclicked) != 0):
					self.setUnmarkedObjs(self.listclicked)
					self.listclicked = []
	
	def mouseMoveEvent(self,event): #zmiana pozycji myszki
		self.mouseGlboalToScenePos(event)
		self.s_mousepos.emit() #wyemitowanie sygnalu o zmianie pozyci
	
	#czy szukany jest najblizszy pkt
		if(self.f_point==True):
			self.nearestrect.setDraw(True) #przed kolejnym pojawieniem sie tego obiektu trzeba zmienic flage 
			self.nearestPoint(self.mousepos[0],self.mousepos[1])
		else:
			self.nearestrect.setDraw(False) #przed kolejnym pojawieniem sie tego obiektu trzeba zmienic flage 
	
	#obsluga tool
		if(self.tool == 0):
			self.Tool0MouseMove()
		if(self.tool == 1): 
			self.Tool1MouseMove()
		elif(self.tool == 2): 
			self.Tool2MouseMove()
		elif(self.tool == 3): 
			self.Tool3MouseMove()
		elif(self.tool == 6):
			self.Tool6MouseMove()
		elif(self.tool == 8):
			self.Tool8MouseMove()
	#aktualizacja sceny
		if(self.f_update == True):
			self.update()
	
#------------ WSZYSTKIE OBIEKTY ------------#
	def swapObj(self,nr1,nr2): #zamienie dwa obiekty miejscami
		tmp = self.obj[nr1] 
		self.obj[nr1] = self.obj[nr2]
		self.obj[nr2] = tmp
		
	def removeObj(self,nr): #usuwa obiekt
		self.s_filechanged.emit()
		self.AddToJourney(1,nr)
		del self.obj[nr]
		self.update()
	
	def removeObjs(self,nrr): #usuwa obiekt
		self.s_filechanged.emit()
		for nr in nrr:
			self.AddToJourney(1,nr)
			del self.obj[nr]
		self.update()
	
	def setMarkedObj(self,nr):#zaznacza obiekt
		self.obj[nr].setMarked()
		self.update()
	
	def setMarkedObjs(self,nrr):#zaznacza obiekty
		for nr in nrr:
			self.obj[nr].setMarked()
		self.update()
	
	def setUnmarkedObj(self,nr):#odznacza obiekt
		self.obj[nr].setUnmarked()
		self.update()
	
	def setUnmarkedObjs(self,nrr):#odznacza obiekt
		for nr in nrr:
			self.obj[nr].setUnmarked()
		self.update()
	
#------------ RYSOWANIE ------------#
	def changedyView(self,dy): #przesyniecie sceny do gory lub w dol
		tmp = self.scenesize[2] + dy
		if(tmp >= 0):
			self.scenesize[2] = tmp
			self.currentview[2] = self.currentview[2] + dy
			self.currentview[3] = self.currentview[3] + dy
			self.update()
		
	def changedxView(self,dx): #przesuniecie sceny w lewo lub w prawo
		tmp = self.scenesize[1] + dx
		if(tmp >= 0):
			self.scenesize[1] = tmp
			self.currentview[0] = self.currentview[0] + dx
			self.currentview[1] = self.currentview[1] + dx
			self.update()
		
	def defaultZoomView(self): #domyslny widok sceny
		self.scenesize[0] = self.defaultview
		
		self.currentview[1] = self.defaultview + self.scenesize[1]
		self.currentview[3] = self.defaultview + self.scenesize[2]
		
		self.update()
		
	def changeZoomView(self,zoom): #przybliza lub oddala scene oraz wysyła odpowiedni sygnal
		if(self.minview < (self.scenesize[0] + zoom) < self.maxview): #sprawdzenie czy zmienna miesci w okreslonym przedziale
			self.scenesize[0] = self.scenesize[0] + zoom 
			
			self.currentview[1] = self.scenesize[0] + self.scenesize[1] #zmiana maksymalnego x + przesuniecie
			self.currentview[3] = self.scenesize[0] + self.scenesize[2] #zmiana maksymalnego y + przesuniecie
			
			self.update() #odswiezenie sceny
		
		#informuje czy bedzie mozliwe nastepne zoomowanie
		if(self.minview >= (self.scenesize[0]+zoom) ):
			self.s_zoomend.emit(0)
		elif(self.maxview <= (self.scenesize[0]+zoom) ):
			self.s_zoomend.emit(1)
		else:
			self.s_zoomend.emit(2)
	
	def draw(self): #funkcja rysujaca wszystkie obiekty 
	#rysowanie obiektow
		for obj in self.obj:
			obj.draw()
	
	#rysowanie tekstu
		if(self.f_text == True):
			self.drawText()
			
		if(self.f_arrows == True):
			self.drawArrows()
			
	#rysowanie prostokata lapiacego 
		self.nearestrect.draw()
	
	def drawText(self): #rysowanie liczb
		glColor3d(153,0,153) #kolor tekstu
		
		i=1
		for obj in self.obj:
		#moge uzyc abs bo rysuje tylko na dodatniej cwiartce
		
			if(obj.f_clikable == True):
				x = (obj.xp + obj.xk)/2
				y = (obj.yp + obj.yk)/2
				
				glRasterPos2f(x,y) #pozycja poczatkowa
				
				txt = str(i)
				
				for character in txt:
					glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord(character))
					
				i = i +1
	
	def drawArrows(self):
		if(len(self.arrows) == 0):
			for obj in self.obj:
				if(obj.f_clikable == True):
					arrow = LocalArrows(obj.xp,obj.yp,obj.xk,obj.yk)
					self.arrows.append(arrow)
		
	#rysowanie grotow
		for obj in self.arrows: 
			obj.draw()
	
	def addLine(self,xp,yp,xk,yk): #dodaje linie do przechowywanych obiektow
		line = LocalLine(xp,yp,xk,yk)
		self.obj.append(line)
		self.s_filechanged.emit()
	
	def addLineXY(self,xp,yp,xk,yk): #dodaje linie do przechowywanych obiektow
		line = LocalLine(xp,yp,xk,yk)
		line.setColorRed()
		self.obj.append(line)
	
	def addRect(self,xp,yp,w,h,mode):
		rect = LocalRect(xp,yp,w,h,mode)
		self.obj.append(rect)
	
#------------ TOOLS (NARZEDZIA) ------------#
	#Zaznaczenie jednego obiektu#
	def Tool0MousePress(self): #na jaki obiekt kliknieto
		#wyczyszczenie poprzednich znaczen
		if(len(self.listclicked) !=0):
			self.setUnmarkedObjs(self.listclicked)
		self.listclicked = []
		
		#sprawdzenie w ktory obj kliknieto
		i=0
		for obj in self.obj:
			test = obj.AmIThere(self.mousepos[0],self.mousepos[1],self.minclickdistance)
			if(test == True):
				self.listclicked.append(i) 
				break #zaznacza pierwsza narysowana linie w tym pkt
			i=i+1
		
		#zaznaczenie obiektow jesli jest taka potrzeba
		if(self.listclicked != 0):
			self.setMarkedObjs(self.listclicked)
	
	def Tool0MouseMove(self):
		if(len(self.listclicked) != 0):
			self.obj[self.listclicked[0]].moveByVector(self.mousepos[0]-self.mouselastclick[0] , self.mousepos[1]-self.mouselastclick[1])
			self.mouselastclick[0] = self.mousepos[0]
			self.mouselastclick[1] = self.mousepos[1]
	
	#Linia#
	def Tool1MouseClick(self):#rysowanie linii
		if(self.f_click == False):#pierwsze klikniecie
			self.f_click = True #znane juz jest polozenie pierwszego klikniecia
			if(self.f_catch == True):
				self.addLine(self.indexcatch[0],self.indexcatch[1],self.indexcatch[0]+0.1,self.indexcatch[1]+0.01) 
			else:
				self.addLine(self.mousepos[0],self.mousepos[1],self.mousepos[0]+0.1,self.mousepos[1]+0.01)
			self.update()
			self.f_update=True #aktualizacja sceny
		elif(self.f_click == True):
			if(self.f_catch == True):
				self.obj[-1].ChangeEndPoint(self.indexcatch[0],self.indexcatch[1])
			self.obj[-1].setColorBlack()
			self.s_filechanged.emit()
			self.s_newobj.emit() 
			self.AddToJourney(0,len(self.obj)-1) 
			self.f_click = False #czeka na kolejne klikniecie
	
	def Tool1MouseMove(self):#zmienia pozycja linii	
		if(self.f_click == True):
			self.obj[-1].ChangeEndPoint(self.mousepos[0],self.mousepos[1])
	
	#Wiele linii#
	def Tool2MouseClick(self):#rysowanie linii
		if(self.f_click == False):#pierwsze klikniecie
			self.f_click = True #znane juz jest polozenie pierwszego klikniecia
			if(self.f_catch == True):
				self.addLine(self.indexcatch[0],self.indexcatch[1],self.indexcatch[0]+0.1,self.indexcatch[1]+0.01) 
			else:
				self.addLine(self.mousepos[0],self.mousepos[1],self.mousepos[0]+0.1,self.mousepos[1]+0.01)
			self.update()
			self.f_update=True #aktualizacja sceny
		elif(self.f_click == True):
			if(self.f_catch == True):
				self.obj[-1].ChangeEndPoint(self.indexcatch[0],self.indexcatch[1])
			self.obj[-1].setColorBlack()
			self.s_newobj.emit() 
			self.s_filechanged.emit()
			#dodanie kolejnej lini
			self.AddToJourney(0,len(self.obj)-1) 
			self.addLine(self.obj[-1].xk , self.obj[-1].yk , self.obj[-1].xk+0.1 , self.obj[-1].yk+0.1)
	
	def Tool2MouseMove(self):#zmienia pozycja linii	
		if(self.f_click == True):
			self.obj[-1].ChangeEndPoint(self.mousepos[0],self.mousepos[1])
	
	#Luk#
	def Tool3MouseClick(self): #rysowanie luku
		if(self.f_click == False):#pierwsze klikniecie
			self.f_click = 1 #znane juz jest polozenie pierwszego klikniecia
			if(self.f_catch == True):
				self.addLine(self.indexcatch[0],self.indexcatch[1],self.indexcatch[0]+0.1,self.indexcatch[1]+0.01) 
			else:
				self.addLine(self.mousepos[0],self.mousepos[1],self.mousepos[0]+0.1,self.mousepos[1]+0.01)
			self.update()
			self.f_update=True #aktualizacja sceny
		elif(self.f_click == 1):
			if(self.f_catch == True):
				self.obj[-1].ChangeEndPoint(self.indexcatch[0],self.indexcatch[1])
				
		#stworzenie luku
			line = self.obj[-1]
			arc = LocalArc(line.xp, line.yp)
			arc.secondpoint(line.xk,line.yk)
			self.removeObj(len(self.obj)-1) #usuniecie lini pomocniczej
			self.obj.append(arc) #dodanie luku do listy
			
			self.f_click = 2 #czeka na kolejne klikniecie
		else:
			self.obj[-1].thirdpoint(self.mousepos[0], self.mousepos[1])
			self.s_newobj.emit() #wyslanie informacji o tym, ze luk zostal stworzony
			self.s_filechanged.emit()
			self.AddToJourney(0,len(self.obj)-1) 
			self.obj[-1].f_active = False
			self.f_click = False
		
	def Tool3MouseMove(self): #modyfikacja rysowanego luku
		if(self.f_click > 0):
			if(self.f_click !=2):
				self.obj[-1].ChangeEndPoint(self.mousepos[0],self.mousepos[1])
			else:
				self.obj[-1].thirdpoint(self.mousepos[0], self.mousepos[1])
	
	#Zaznaczenie wielu obiektow#
	def Tool6MouseClick(self): #zaznaczaenie wielu obiektow - rysowanie
		if(self.f_click == False): #pierwsze klikniecie - tworzenie prostokata
			rect =  SelectRect(self.mousepos[0],self.mousepos[1]) #stworzenie prostokata
			self.obj.append(rect) #dodanie prosotkau do listy obiektow
			self.f_click = True #pierwsza pozycja klikniecia znana
			self.f_update = True #aktualizuj prostokat w momencie ruchu myszka
		else:
			self.f_update = False #wylaczenie aktualizacji w momencie ruchu myszka
			
			if(len(self.listclicked) !=0): #odzaczenie ewentualnie zaznaczonych obiektow
				self.setUnmarkedObjs(self.listclicked)
			self.listclicked = [] #wyczyszczenie listy 
			
			i=0
			rect = self.obj[-1] #wybranie stworzonego prosotkatu
			rect.setxy() #odpowiednie ustawienie zmiennych xp ma byc mniejsze od xk i yp od yk - potrzebne do pozniejszych testow
			while(i<len(self.obj)-1): #testowanie wszystkich obiektow
				test = False #wartosc poczatkowa testu - czy zaznaczac obiekt
				obj = self.obj[i] #wybor testowanego obiektu
				
				if(obj.f_clikable == True): #czy obiekt jest zaznaczalny
					if(obj.WhatAmITxt() == "Linia"): #test wylacznie dla lini
						test = rect.LiangBarsky(obj.xp, obj.yp , obj.xk , obj.yk)
						
					if(test == True): #dodanie obiektu do listy 
						self.listclicked.append(i) 
						
				
				i=i+1 
			self.removeObj(len(self.obj)-1) #usuwa prostokat sluzacy do zaznaczania
			self.f_click = False 
			
			if(self.listclicked != 0): #zaznaczenie obiektow
				self.setMarkedObjs(self.listclicked)
		
	def Tool6MouseMove(self): #odswiezanie pozycji dla zaznaczenia wielu obiektow
		if(self.f_click  == True):
			self.obj[-1].ChangeEndPoint(self.mousepos[0],self.mousepos[1])
	
	#zmiana wielkosci
	def Tool8MouseClick(self): #wydluzanie
		if(len(self.listclicked) != 0):
			self.setUnmarkedObjs(self.listclicked)
		
		self.listclicked = [] 
		
		if(self.f_click == False):
			if(self.f_catch == True):
				self.mouselastclick = self.mousepos
				i=0
				for obj in self.obj:
					if(obj.f_clikable == True):
						if( obj.checkPoint(self.indexcatch[0], self.indexcatch[1],self.minclickdistance) == True):
							obj.setColorBlue()
							self.listclicked.append(i)
					i=i+1
				self.f_click = True
				self.f_update = True
		elif(self.f_click == True):
			self.f_click = False
			self.f_update = False
	
	def Tool8MouseMove(self): 
		if(self.f_click == True):
			for nr in self.listclicked:
				self.obj[nr].ChangePoint(self.mousepos[0],self.mousepos[1])
		
	#sciaga
	def WhatDoesTool(self): #opis narzedzi, ta funkcja pozniej zostanie usunieta
		#tool0 - klikanie na pojedynczy obiekt na scenie
		#tool1 - linia o poczatku klik i koncu klik
		#tool2 - jak tool1 tyle ze kolejna linia rysowana jest z poprzedniego pkt
		#tool3 - luk 3pkt
		#tool4 - sortowanie obiektow
		#tool5 - linia + kat (moze bedzie do wycofania)
		#tool6 - zaznaczanie wielu obiektow na scenie
		#tool7 - strzalki informujace o poczatku i koncu wszystkich obiektow
		#tool8 - przesuwanie pkt
		pass
	
	#ustawienie narzedzia 
	def setTool(self,nr): #dzieki temu, ze uzwam setTool moge ustawic flagi zaraz po wybraniu narzedzia bez koniecznosci odbierania sygnalu
		self.tool = nr #ustawia narzedzie
		self.arrows = []
		if(1 <= nr <= 3)or(nr == 8):
			self.f_point = True
			self.f_text  = False
			self.f_arrows = False
		
		elif(nr == 4): #lista
			self.f_text  = True
			self.f_arrows = True
			
	def cancelDraw(self): #anuluj
		if(self.tool == 0): #przesuwanie obiektu
			if(len(self.listclicked)!=0):
				self.obj[self.listclicked[0]].moveByVector(-self.mousepos[0]+self.mouselastclick[2] , -self.mousepos[1]+self.mouselastclick[3])
				self.mouselastclick[0] = self.mousepos[0]
				self.mouselastclick[1] = self.mousepos[1]
		elif(self.obj[-1].f_active == True): #objekt jest wlasnie rysowany
			self.flags() #ustawia flagi domyslnie
			self.setTool(self.tool) #ustawia flagi na powrot dla danego narzedzia jesli to konieczne
			self.removeObj(len(self.obj)-1) #usuwa obiekt ze sceny
			
		#usuniecie tej informacji z kroniki
			del self.journey[-1]
			self.journeycurrent =self.journeycurrent - 1
			
			self.update() #przerysuwuje
	
#------------ KRONIKA ------------#
	def AddToJourney(self,what,nr): #co ostatnio stalo sie z obiektem
		obj = self.obj[nr]
		self.journeycurrent = self.journeycurrent + 1
		
		if(obj.WhatAmITxt() == "Linia"):
			tmp = [what,obj.WhatAmITxt(),nr, obj.xp,obj.yp,obj.xk,obj.yk]
			self.journey.append(tmp)
			
		elif(obj.WhatAmITxt() == "Luk"):
			tmp = [ what, obj.WhatAmITxt(), nr, obj.xp,obj.yp, obj.xk, obj.yk , obj.x3, obj.y3 ]
			self.journey.append(tmp)
		
		if(self.journeycurrent == 0):
			self.s_previous.emit(True)
	
	def previousStepJourney(self): #poprzedni krok
		if(self.journeycurrent != -1):
			step = self.journey[self.journeycurrent]
			whatobj = step[1]
			whathappend = step[0]
			nr = step[2] #nr na liscie
			if(whatobj == "Linia"):
				if(whathappend == 0): #usun mnie
					del self.obj[nr]
					
				elif(whathappend == 1): #dodanie nowej lini
					line = LocalLine(step[3], step[4], step[5], step[6])
					self.obj.insert(nr, line)
					self.obj[nr].setColorBlack()
				
			elif(whatobj == "Luk"):
				if(whathappend == 0):
					del self.obj[nr]
				elif(whathappend == 1):
					arc = LocalArc(step[3], step[4])
					arc.secondpoint(step[5], step[6])
					arc.thirdpoint(step[7], step[8])
					arc.setColorBlack()
					self.obj.insert(nr,arc)
				
			self.journeycurrent = self.journeycurrent - 1 
			
			if(self.journeycurrent == len(self.journey)-2):
				self.s_next.emit(1)
			
			if(self.journeycurrent == -1):
				self.s_previous.emit(0) #emituje sygnal inf. o tym, ze nie ma poprzedniego elemtu na liscie
			
			self.update() #aktualizacja sceny
	
	def nextStepJourney(self): #nastpeny krok
		if(self.journeycurrent != len(self.journey)-1):
			self.journeycurrent = self.journeycurrent + 1
			obj = self.journey[self.journeycurrent]
			whatObject = obj[1]
			whatHappend = obj[0]
			nr = obj[2]
		
		#czesc wlasciwa
			if(whatObject == "Linia"):
				if(whatHappend == 1):  #usuniecie obiekty
					del self.obj[nr]
				
				elif(whatHappend == 0): #dodanie obiektu
					line = LocalLine(obj[3], obj[4], obj[5], obj[6])
					line.setColorBlack()
					self.obj.insert(nr,line)
					
			elif(whatObject == "Luk"):
				if(whatHappend == 1):
					del self.obj[nr]
				elif(whatHappend == 0):
					arc = LocalArc(obj[3], obj[4])
					arc.secondpoint(obj[5], obj[6])
					arc.thirdpoint(obj[7], obj[8])
					arc.setColorBlack()
					self.obj.insert(nr,arc)
					
		#modyfikacja akcji
			if(self.journeycurrent == len(self.journey)-1):
				self.s_next.emit(0)
			
			if(self.journeycurrent == 0):
				self.s_previous.emit(1)
			
			self.update() 
	
#------------ ZAPISZ DXF ------------#
	def DXFSaveLine(self,obj): #format DXF Lini
		txt = "LINE\n"
		
		#wspolrzedne poczatkowe
		txt +="10\n" #informuje ze nastepny znak oznaczac bedzie xp
		txt += str(obj.xp)+"\n"
		txt +="20\n" #informuje ze nastepny znak oznaczac bedzie yp
		txt += str(obj.yp)+"\n"
		
		#wspolrzedne koncowe
		txt +="11\n" #informuje ze nastepny znak oznaczac bedzie xk
		txt += str(obj.xk)+"\n"
		txt +="21\n" #informuje ze nastepny znak oznaczac bedzie yk
		txt += str(obj.yk)+"\n"
		txt +="0\n" #zakonczenie sekcji lini
		
		return txt
		
	def DXFSaveArc(self,obj): #format DXF Luku
	#Typ
		txt = "ARC\n"
		
	#wspolrzedne srodka
		txt +="10\n" #informuje ze nastepny znak oznaczac bedzie xp
		txt += str(obj.x)+"\n"
		txt +="20\n" #informuje ze nastepny znak oznaczac bedzie yp
		txt += str(obj.y)+"\n"
		txt +="40\n"#informuje o tym ze nastepny znak bedzie oznaczac promien
		txt += str(obj.R)+"\n"
		
	#katy
		txt +="50\n"#informuje o tym ze nastepny znak bedzie oznaczac kat poczatkowy
		txt += str(obj.degreebegin)+"\n"
		#txt += str(obj.degreeend)+"\n"
		txt +="51\n"#informuje o tym ze nastepny znak bedzie oznaczac kat koncowy
		txt += str(obj.degreeend)+"\n"
		#txt += str(obj.degreebegin)+"\n"
	#zakonczenie
		txt +="0\n" #zakonczenie sekcji lini
		return txt
	
	def DXFSave(self,fname): #zapis pliku do foramtu dxf
		try:
			with open(fname,"w") as outfile:
				#naglowek
				txt = "  0\nSECTION\n2\nHEADER\n"
				
				#komentarze pycadowe :P
			
				txt += "999\n" #inormuje ze jest to komentarz
				txt += "utworzone przez pycad\n" 
				txt += "999\n" #inormuje ze jest to komentarz
				txt += str(datetime.now()) + "\n"
				txt += "0\nENDSEC\n0\n"
				
				#niezbedne struktury
				txt += "SECTION\n2\nTABLES\n0\nENDSEC\n0\nSECTION\n2\nBLOCKS\n0\nENDSEC\n0\nSECTION\n2\nENTITIES\n0\n"
				outfile.write(txt)
				
				for obj in self.obj:
					
					if(obj.f_clikable == True): #flaga informujaca o tym, czy nie ignorowac obiektu
						
						txt = ""
						
						if(obj.WhatAmITxt() == "Linia"): 
							txt = self.DXFSaveLine(obj)
							
						elif(obj.WhatAmITxt() == "Luk"):
							txt = self.DXFSaveArc(obj) 
							
						if(txt != ""):
							outfile.write(txt)
							
				#stopka
				txt = "ENDSEC\n0\nEOF" 
				outfile.write(txt)
				
				outfile.close() #zamkniecie pliku
				return True
		except:
			print "Zapis nie powidol sie"
			return False
	
#------------ WCZYTAJ ------------#
	def DXFLoadLine(self,f,txtline): #wczytywanie lini o formacie DXF 
		fok = True
		read = True 
		error = "" #tresc bledu
		
		variablesrequired =["xp","xk","yp","yk"] #nazwy potrzebnych zmiennych
		variablesread = 0 #przeczytane zmienne
		
		while(read == True)and(txtline)and(variablesread != len(variablesrequired)):
			txtline = f.readline()
			txtline=txtline.replace("\n","").replace("\t","")
			
		#wspolrzedne poczatkowe:
			if(txtline =='10'): #x
				txtline = f.readline()
				txtline = txtline.replace("\n","").replace("\t","")
				
			#sprawdzenie czy zmienna nie zostala juz przypisana, jesli tak to blad w pliku
				if 'xp' in locals():
					error += "xp\n"
					read = False
				else:
					xp = float(txtline) #odczytuje xp
					variablesread = variablesread + 1
					
			elif(txtline =='20'): #y
				txtline = f.readline()
				txtline = txtline.replace("\n","").replace("\t","")
					
			#sprawdzenie czy zmienna nie zostala juz przypisana, jesli tak to blad w pliku
				if 'yp' in locals():
					error += "yp\n"
					read = False
				else:
					yp = float(txtline) #odczytuje yp
					variablesread = variablesread + 1
					
		#wspolrzedne koncowe:
			elif(txtline =='11'): #xk
				txtline = f.readline()
				txtline = txtline.replace("\n","").replace("\t","")
				
			#sprawdzenie czy zmienna nie zostala juz przypisana, jesli tak to blad w pliku
				if 'xk' in locals():
					error += "xk\n"
					read = False
				else:
					xk = float(txtline) #odczytuje xk
					variablesread = variablesread + 1
				
			elif(txtline =='21'): #yk
				txtline = f.readline()
				txtline = txtline.replace("\n","").replace("\t","")
				
			#sprawdzenie czy zmienna nie zostala juz przypisana, jesli tak to blad w pliku
				if 'yk' in locals():
					error += "yk\n"
					read = False
				else:
					yk = float(txtline) #odczytuje yk
					variablesread = variablesread + 1
					
		#koniec pliku (wg standardu)
			elif(txtline =='EOF'):
				read = False
				break
				
		if(variablesread != len(variablesrequired)): #jakich zmiennych brakuje
			fok = False
			for vname in variablesrequired:
				if not(vname in locals()):
					error += "brakuje zmiennej " + str(vname) + "\n"
		else:
			if(read == True):
				try:
					#print xp,yp,xk,yk
					localline = LocalLine(xp,yp,xk,yk)
					localline.setColorBlack()
					self.obj.append(localline)
				except:
					error += "nie mozna utworzyc localline - blednie wczytane zmienne\n"
					fok = False
			else:
				fok = False
				
		return [fok,error]
	
	def DXFLoadArc(self,f,txtline): #wczytywanie lukow o formacie DXF
		fok = True
		read = True 
		error = "" #tresc bledu
		
		variablesrequired =["x","y","R","degreebegin","degreeend"] #nazwy potrzebnych zmiennych
		variablesread = 0 #przeczytane zmienne
		
		while(read == True)and(txtline)and(variablesread != len(variablesrequired)):
			txtline = f.readline()
			txtline=txtline.replace("\n","").replace("\t","")
			
		#wspolrzedne srodka:
			if(txtline =='10'): #x
				txtline = f.readline()
				txtline = txtline.replace("\n","").replace("\t","")
				
			#sprawdzenie czy zmienna nie zostala juz przypisana, jesli tak to blad w pliku
				if 'x' in locals():
					error += "x\n"
					read = False
				else:
					x = float(txtline) #odczytuje xp
					variablesread = variablesread + 1
					
			elif(txtline =='20'): #y
				txtline = f.readline()
				txtline = txtline.replace("\n","").replace("\t","")
				
			#sprawdzenie czy zmienna nie zostala juz przypisana, jesli tak to blad w pliku
				if 'y' in locals():
					error += "y\n"
					read = False
				else:
					y = float(txtline) #odczytuje xp
					variablesread = variablesread + 1
					
		#dlugosc promienia (R)
			elif(txtline =='40'): #y
				txtline = f.readline()
				txtline = txtline.replace("\n","").replace("\t","")
				
			#sprawdzenie czy zmienna nie zostala juz przypisana, jesli tak to blad w pliku
				if 'R' in locals():
					error += "R\n"
					read = False
				else:
					R = float(txtline) #odczytuje xp
					variablesread = variablesread + 1
					
		#katy
			elif(txtline =='50'): #kat poczatkowy
				txtline = f.readline()
				txtline = txtline.replace("\n","").replace("\t","")
				
			#sprawdzenie czy zmienna nie zostala juz przypisana, jesli tak to blad w pliku
				if 'degreebegin' in locals():
					error += "degreebegin\n"
					read = False
				else:
					degreebegin = float(txtline) #odczytuje xp
					variablesread = variablesread + 1
					
			elif(txtline =='51'): #kat koncowy
				txtline = f.readline()
				txtline = txtline.replace("\n","").replace("\t","")
				
			#sprawdzenie czy zmienna nie zostala juz przypisana, jesli tak to blad w pliku
				if 'degreeend' in locals():
					error += "degreeend\n"
					read = False
				else:
					degreeend = float(txtline) #odczytuje xp
					variablesread = variablesread + 1		
					
		#koniec pliku (wg standardu)
			elif(txtline =='EOF'):
				read = False
				break
				
		if(variablesread != len(variablesrequired)): #jakich zmiennych brakuje
			fok = False
			for vname in variablesrequired:
				if not(vname in locals()):
					error += "brakuje zmiennej " + str(vname) + "\n"
		else:
			if(read == True):
				try:
					xp = R * cos(radians(degreebegin))
					yp = R * sin(radians(degreebegin))
					xk = R * cos(radians(degreeend))
					yk = R * sin(radians(degreeend))
					arc = LocalArc(xp,yp)
					arc.secondpoint(xk,yk)
					arc.x = x
					arc.y = y
					arc.R = R
					arc.degreebegin = degreebegin
					arc.degreeend = degreeend
					arc.f_draw = True
					arc.reCalcArray()
					arc.setColorBlack()
					self.obj.append(arc)
				except:
					error += "nie mozna utworzyc LocalArc - bledne zmienne\n"
					fok = False
			else:
				fok = False
				
		return [fok,error]
	
	def DXFLoad(self,fname): #wczytywanie calego pliku DXF
		f = open(fname, 'r') #otwarcie lini
		txtline = f.readline() #przeczytanie pierwszej linii
		fok = True  #flaga ktora inforume o tym czy plik jest zgodny z formatem
		
		while txtline:
			txtline=txtline.replace("\n","").replace("\t","")
			#txtline=txtline.replace("\t","")
			
			if(txtline == "LINE"): #linia
				tmp = self.DXFLoadLine(f,txtline)
				fok = fok * tmp[0] 
			#drukuje blad
				if(tmp[0] == False):
					print tmp[1] 
				
			elif(txtline == "ARC"): #Luk
				tmp = self.DXFLoadArc(f,txtline)
				fok = fok * tmp[0] 
			#drukuje blad
				if(tmp[0] == False):
					print tmp[1] 
				
			txtline = f.readline() #czyta kolejna linie
		f.close()
		
		return fok
	
#------------ FUNKCJE WSPOMAGAJACE OBLICZENIA ------------#
	def distance(self,x,y,x2,y2): #odleglosc miedzy dwoma punktami
		return (((x-x2))**2+((y-y2)**2))**0.5
	
	def setMinDstance(value): #zmienia minlana odleglosc ktora wykryje nearestPoint
		if(value >=0):
			self.mindistance = value
	
	def nearestPoint(self,x,y): #szuka najblizszego pkt
		self.f_catch = False
		
		if(self.mindistance > 0): 
		#poczatkowe wartosci
			distance = self.mindistance
			distancePoint = [0,0]
			i=0
			
		#sprawdzenie ktory obiekt jest najblizej
			for obj in self.obj:
				if(obj.f_active == False): #pomija aktywne obiekty
					what = obj.WhatAmITxt()
					if(what == "Linia")or(what == "Luk"): #linia
						#wspolrzedne poczatkowe
						value = self.distance(obj.xp,obj.yp,x,y)
						if(value < distance):
							distance = value
							distancePoint = (obj.xp,obj.yp)
							
						#wspolrzedne koncowe
						value = self.distance(obj.xk,obj.yk,x,y)
						if(value < distance):
							distance = value
							distancePoint = (obj.xk,obj.yk)
				i=i+1
				
		#sprawdzenie czy znaleziony obiekt miesci sie w podanym limicie
			if(self.mindistance > distance):
				self.f_catch = True #ustawienie flagi
				self.indexcatch = distancePoint #znalezione wsp
				self.nearestrect.newxy(self.indexcatch[0],self.indexcatch[1],self.mindistance*4)
				self.nearestrect.setDraw(True)
				self.update()
			else:
				self.nearestrect.setDraw(False)
