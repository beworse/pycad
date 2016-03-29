#!/usr/bin/python
# -*- coding: utf-8 -*-

#----------------------------------------------------------------------#
#CELE TEGO PLIKU:
#- Tworzenie i modyfikowanie lini
#----------------------------------------------------------------------#

#podstawoe biblioteki pythona
import sys #System-specific parameters and functions
import os # Miscellaneous operating system interfaces
import string #Common string operations
from math import * #Mathematical functions

#biblioteka opengl
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

class LocalArrows(): #rysuje groty strzalek
	def __init__(self,xp,yp,xk,yk): 
		self.variables(xp,yp,xk,yk)
		
	def variables(self,xp,yp,xk,yk):
	#stale strzalek
		length = 0.05 #dlugosc grotu
		anglearrow = 10 #kat strzalki
		linelength = 0.1 #dlugosc lini w stosunku do prawdziwej
		
		angleline = atan2(yk-yp,xk-xp) #kat lini
		
	#zmienne grotow
		self.up = [xk, yk, xk + cos(angleline + anglearrow)*length, yk + sin(angleline + anglearrow)*length]
		self.down = [xk, yk, xk + cos(angleline - anglearrow)*length, yk+ sin(angleline - anglearrow)*length]
		
	def draw(self): #rysowanie
		glColor3d(102,0,0) #kolor
		glBegin(GL_LINE_LOOP) 
		
	#grot gora
		glVertex2f(self.up[0],self.up[1])
		glVertex2f(self.up[2],self.up[3])
		
	#grot dol
		glVertex2f(self.down[0],self.down[1])
		glVertex2f(self.down[2],self.down[3])
		glEnd()
		
	def distance(self,x,y,x2,y2): #odleglosc miedzy dwoma punktami
		return (((x-x2))**2+((y-y2)**2))**0.5

class Colors(): #pomysl na nowa klase do przemyslenia, poki co nie jest wykorzystywana
	def __init__(self): 
		#klasa zawiera trzy zmienne r,g,b
		self.setColorBlack() #domyslny kolor
		
		
	def setColorBlack(self): 
		self.r = 0
		self.g = 0
		self.b = 0
	
	def setColorRed(self):
		self.r = 1
		self.g = 0
		self.b = 0
	 
	def setColorBlue(self):
		self.r = 0
		self.g = 0
		self.b = 1
		
	def setColorGreen(self): 
		self.r = 0
		self.g = 1
		self.b = 0
		
	def setOtherColor(self):
		pass
	
class LocalArc():#rysowanie lukow
#------------ INCJALIZACJA ------------#
	def __init__(self,xp,yp):#inicjalizacja
		self.variables(xp,yp)
		self.flags()
		self.setColorBlue()
		
	def variables(self,xp,yp): #zmienne
	#wsp pierwszego klikniecia
		self.xp = xp 
		self.yp = yp
		
	#wsp drugiego klikniecia
		self.xk = xp 
		self.yk = yp
		
	#wsp trzeciego klikniecia
		self.x3 = xp
		self.y3 = yp
		
	#katy
		self.degreebegin = 0
		self.degreeend = 0
	
	#do rysownia
		self.array = [] #tablicy linii
		self.n = 20 #dlugos tablicy
	
	def flags(self):#flagi
		self.f_draw = False #jesli flaga nie jest ustawiona nic nie zostanie narysowane
		self.f_active = True #jest rysowany
		self.f_clikable = True #czy mozna kliknac w ten obiekt
		self.f_marked = False
	
#------------ RYSOWANIE ------------#
	def draw(self): #tworzenie obiektu
		if(self.f_draw == True): #jesli falga nie jest rysowana obiekt nie zostanie narysowany
			glBegin(GL_LINE_LOOP) #laczy linie
			glColor3d(self.r , self.g ,self.b*0) #kolor
			for obj in self.array:
				glVertex2f(obj[0], obj[1]) 
			glEnd() #koniec rysowania
	
#------------ KOLORY ------------#
	def setColorBlack(self): #stwrzony
		self.r = 0
		self.g = 0
		self.b = 0
	
	def setColorGreen(self): #zaznaczenie
		self.r = 0
		self.g = 1
		self.b = 0
		
	def setColorBlue(self): #rysowanie
		self.r = 0
		self.g = 0
		self.b = 1
	
#------------ MODYFIKACJA ZMIENNYCH ------------#
	def secondpoint(self,x,y): #drugie klikniecie
		self.xk = x 
		self.yk = y
	
	def thirdpoint(self,x,y): #trzecie klikniecie oraz obliczenie parametrow luku
		self.x3 = x
		self.y3 = y
		self.calcArc(self.xp,self.yp , self.x3,self.y3, self.xk,self.yk)
	
	def moveByVector(self,x,y):
		self.xp = self.xp + x
		self.yp = self.yp + y
		
		self.xk = self.xk + x
		self.yk = self.yk + y
		
		self.x3 = self.x3 + x
		self.y3 = self.y3 + y
		
		self.calcArc(self.xp,self.yp , self.x3,self.y3, self.xk,self.yk)
	
#------------ OBLICZENIOWE ------------#
	def calcAB(self): #oblicza A,B dla wzoru y=Ax+B
		if((self.xp-self.xk) != 0):
			self.A = (self.yp-self.yk) / (self.xp-self.xk)
			self.B = self.yk - (self.A*self.xk)
		elif(self.xp != 0):
			self.A = self.yp/self.xp
			self.B = 0
		elif(self.xk != 0):
			self.A = self.yk/self.xk
			self.B = 0
		else:
			self.A = 0
			self.B = 0

	def sideofLine(self,x,y):
		y2 = x*self.A+self.B
		if(y2 == y):
			return 0
		elif(y2 > y):
			return 1
		else:
			return -1
		
	def reCalcArray(self):
		ang = self.degreeend - self.degreebegin
		ang = ang/self.n
		i=0
		self.array = []
		
		while(i<=self.n):
			
			d = ( i*ang ) + self.degreebegin
			
			x = self.R * cos(radians(d))
			y = self.R * sin(radians(d))
			
			self.array.append([self.x+x,self.y+y])
			i=i+1
		
	def calcArray(self): #stworzenie tablicy do narysowania luku
		self.array = []
	
	#obliczenie katow
		self.degreebegin = degrees(atan2(self.yp-self.y,self.xp-self.x))
		self.degreeend = degrees(atan2(self.yk-self.y,self.xk-self.x))
		ang = self.degreeend - self.degreebegin
		
	#obliczenie wspolrzednych do testu
		d = (ang/self.n)+self.degreebegin
		x = self.R*cos(radians(d))+self.x
		y = self.R*sin(radians(d))+self.y
		
	#sprawdzenie czy pkt lezy po tej samej stronie, co ostatnie klikniecie
		self.calcAB()
		if(self.sideofLine(x,y) != self.sideofLine(self.x3,self.y3)):
			#obliczenie nowego kata
			 tmp = 180 + (180- abs(self.degreebegin))
			 tmp = copysign(tmp, -self.degreebegin) #skopiowanie przeciwnego znaku
			 self.degreebegin = tmp #ustawienie nowego kata poczatkowego
			 self.degreeend = degrees(atan2(self.yk-self.y,self.xk-self.x)) #wyliczenie nowego konta koncowego
			 ang  = self.degreeend - self.degreebegin #obliczenie nowej odleglosci katwoej
			 
		ang = ang/self.n
		i=0
		while(i<=self.n):
			d = ( i*ang ) + self.degreebegin
			x = self.R * cos(radians(d))
			y = self.R * sin(radians(d))
			self.array.append([self.x+x,self.y+y])
			i=i+1
		
	def calcArc(self,x1,y1,x2,y2,x3,y3): #obliczenie wsp srodka oraz promienia a takze kata poczatkowego i koncowego
		down = y1 * x3 - y1 * x2 - y2 * x3 - y3 * x1 + y3 * x2 + y2 * x1 #mianownik
		if(down != 0):
		#obliczneie polozenia srodka
			self.x = 0.5 * ((x2 * x2 * y3 + y2 * y2 * y3 - x1 * x1 * y3 + x1 * x1 * y2 - y1 * y1 * y3 + y1 * y1 * y2 + y1 * x3 * x3 + y1 * y3 * y3 - y1 * x2 * x2 - y1 * y2 * y2 - y2 * x3 * x3 - y2 * y3 * y3) / (down))
			self.y = 0.5 * ((-x1 * x3 * x3 - x1 * y3 * y3 + x1 * x2 * x2 + x1 * y2 * y2 + x2 * x3 * x3 + x2 * y3 * y3 - x2 * x2 * x3 - y2 * y2 * x3 + x1 * x1 * x3 - x1 * x1 * x2 + y1 * y1 * x3 - y1 * y1 * x2) / (down))
			
		#oblicznie dlugosci promienia (moznaby podstawic do innego wzoru ale ten jest prostszy)
			self.R = (((self.x-x1)**2) + ((self.y-y1)**2))**(0.5)
			
			self.calcArray()
			self.f_draw = True
		else:
			self.f_draw = False
	
#------------ ZWRACANIE INFROMACJI ------------#
	def WhatAmILongTxt(self):
		if(self.f_draw == True):
			return "Luk r("+ str(self.x) + str(self.y) + ")"
		else:
			return "Luk niemozliwy do narysownia"
	
	def WhatAmITxt(self): 
		return "Luk"
	
	def setMarked(self): #zaznacza linie
		self.setColorGreen()
		self.f_marked = True
	
	def setUnmarked(self): #odnacza linie
		self.setColorBlack()
		self.f_marked = False
	
	def AmIThere(self,xt,yt,dx): #test dla klikniecia w luk
		if(self.sideofLine(xt,yt) == self.sideofLine(self.x3, self.y3)): #sprawdzenie czy ostatnie klikniecie jest po tej samie stronie co klikniecie
			r = sqrt(((xt - self.x)**2)+((yt - self.y)**2))
			if( (r - dx) <= self.R <= (r + dx)): #sprawdzenie czy klikniecie lezy na promieniu
				return True
		else: #sprawdzenie czy pkt lezy na lini
			ydpp = self.A*xt+(self.B-dx)
			ydpm = self.A*xt+(self.B+dx)
			if(ydpm <= yt <= ydpp): 
				return True 
			elif(ydpm >= yt >= ydpp): 
				return True 
			return False 
		return False
	
class NearestPointRect(): #prosotkat do zaznaczania najblizszego pkt
#------------ INCJALIZACJA ------------#
	def __init__(self,x,y,length): #inicjalizcja x,y to srodek prostokatu
		self.variables(x,y,length)
		self.setColorBlack()
		self.flags()
	
	def variables(self,x,y,length): #zmienne
		self.x = x #srodek wsp x
		self.y = y #srodek wsp y
		
		self.length = abs(length) #dl boku
		hl = self.length*0.5 #polowa dlugosci
		
		#wspolrzedne 
		self.xp = x - hl 
		self.yp = y - hl
		self.xk = x + hl
		self.yk = y + hl
	
	def flags(self): #wykorzytane flagi 
		self.f_draw = False #czy rysowac
	
#------------ MODYFIKACJA ZMIENNYCH ------------#
	def newxy(self,x,y,length): #ustawia nowe wsp
		if(self.x != x)or(self.y != y)or(self.length != length): #test czy cos uleglo zmianie
			self.variables(x,y,length)
	
	def setDraw(self,test): #ustawia flage do rysowania
		self.f_draw = test
	
#------------ RYSOWANIE ------------#	
	def draw(self): #tworzenie obiektu
		if(self.f_draw == True): #jesli falga nie jest rysowana obiekt nie zostanie narysowany
			glBegin(GL_LINES) #rodzaj rysowania
			#glScalef(0.01,0.01,1)
			#glEnable (GL_LINE_STIPPLE)
			#glLineStipple (1, 0x00FF)
			glColor3d(self.r,self.g,self.b) #kolor
		#pierwsza linia - dolna
			glVertex2f(self.xp, self.yp) 
			glVertex2f(self.xk, self.yp) 
		#druga linia - prawa
			glVertex2f(self.xk, self.yp) 
			glVertex2f(self.xk, self.yk) 
		#trzecia linia - gora
			glVertex2f(self.xk, self.yk) 
			glVertex2f(self.xp, self.yk) 
		#czwarta linia - lewa
			glVertex2f(self.xp, self.yk) 
			glVertex2f(self.xp, self.yp) 
			#glDisable (GL_LINE_STIPPLE)
			glEnd() #koniec rysowania
			
	
#------------ KOLORY ------------#
	def setColorBlack(self): #kolor
		self.r = 0
		self.g = 0
		self.b = 0
	
#------------ ZWRACANIE INFROMACJI ------------#
	def WhatAmITxt(self): 
		return "Prostokat najblizszego pkt"
	
class SelectRect():#klasa sluzaca do zaznaczania
#------------ INCJALIZACJA ------------#
	def __init__(self,xp,yp): #inicjalizcja
		self.variables(xp,yp)
		self.flags()
		self.setColorBlack()
		self.draw()
		
	def variables(self,xp,yp): #zmienne
		self.xp = xp
		self.yp = yp
		self.xk = xp+0.001
		self.yk = yp+0.001
		
	def flags(self): #wykorzytane flagi 
		self.f_active = True #obiekt jest aktualnie rysowany, flaga ta nie ulegnie zmianie ze wzgledu na to ze z zalozenia obiekt ma zostac zniszczony zaraz po jego wykorzystaniu
		self.f_clikable = False #obiekt bedzie ignorowal klikniecie
		
#------------ MODYFIKACJA ZMIENNYCH ------------#
	def ChangeEndPoint(self,xk,yk):#metoda do ustawienia xk oraz yk 
		self.xk = xk
		self.yk = yk
	
	def setxy(self): #zmienia kolejnosc xp z xk oraz yp z yk jesli zachodzi taka koniecznosc
		if(self.xp > self.xk):
			xk = self.xp
			self.xp = self.xk
			self.xk = xk
		if(self.yp > self.yk):
			yk = self.yp
			self.yp = self.yk
			self.yk = yk
		self.h = abs(self.xp - self.xk)
		self.w = abs(self.yp - self.yk)
		
#------------ RYSOWANIE ------------#	
	def draw(self): #tworzenie obiektu
		glBegin(GL_LINES) #rodzaj rysowania
		#glScalef(0.01,0.01,1)
		#glEnable (GL_LINE_STIPPLE)
		#glLineStipple (1, 0x00FF)
		glColor3d(self.r,self.g,self.b) #kolor
	#pierwsza linia - dolna
		glVertex2f(self.xp, self.yp) 
		glVertex2f(self.xk, self.yp) 
	#druga linia - prawa
		glVertex2f(self.xk, self.yp) 
		glVertex2f(self.xk, self.yk) 
	#trzecia linia - gora
		glVertex2f(self.xk, self.yk) 
		glVertex2f(self.xp, self.yk) 
	#czwarta linia - lewa
		glVertex2f(self.xp, self.yk) 
		glVertex2f(self.xp, self.yp) 
		#glDisable (GL_LINE_STIPPLE)
		glEnd() #koniec rysowania
	
#------------ ZWRACANIE INFROMACJI ------------#
	def WhatAmILongTxt(self): #czym jestem wersja dluzsza
		return "Prostokat ("+str(self.xp)+","+str(self.yp)+") ("+str(self.xk)+","+str(self.yk)+")"
	
	def WhatAmITxt(self): #czym jestem
		return "Prostokat"
	
#------------ KOLORY ------------#
	def setColorBlack(self): #kolor czarny
		self.r = 0
		self.g = 0
		self.b = 0
	
#------------ ZAZNACZENIA ------------# #metody sluzace do sprawdzenia kolizji
	def LiangBarsky(self,xp,yp,xk,yk): #Liang-Barsky - czyli sprowadzenie 2D - 1D 
		t0 = 0
		t1 = 1
		dx = xk - xp
		dy = yk - yp
		
		i = 0
		while(i < 4):
			#wybor krawedzi
			if(i == 0) :
				p = -dx
				q = -(self.xp - xp)
			elif(i == 1): 
				p = dx
				q = self.xk - xp
			elif(i == 2):
				p = -dy
				q = -(self.yp - yp)
			elif( i==3 ):
				p = dy
				q = self.yk -yp
			
			r = q/p
			
			if(p == 0)and(q < 0):
				return False
			
			if(p < 0):
				if(r > t1):
					return False
				elif(r>t0):
					t0 = r
					
			elif( p > 0 ):
				if(r<t0):
					return False
					
				elif(r < t1 ):
					t1 = r
			i=i+1
			
		#znalezione pkt przeciecia
		#xf = xp + t0*dx
		#xf2 = xp + t1*dx
		#yf = yp + t0*dy
		#yf2 = yp + t1*dy
		
		return True
		 
	def CohenSutherlandCode(self,x,y): #generowanie kodow do funkcji CohenSutherland
		code = 0b000 #srodek
		
		#polozenie x
		if( x < self.xp ):
			code = code | 0b0001 #z lewej
		elif( x > self.xk):
			code = code | 0b0010 #z prawej
		
		#polozenie y
		if( y < self.yp):
			code = code | 0b0100 #na dole
		elif( y > self.yk):
			code = code | 0b1000 #u gory
		
		return code
	
	def CohenSutherland(self, a1, a2, b1, b2):  #mozna wykorzsytac do zaznaczanie obiektow ktore sa wewnatrz
	#wartosc poczatkowa
		accept = False
		out = 0b0000
		xp = a1
		yp = a2
		xk = b1 
		yk = b2
	
	#obliczenie kodow Cohena-Suherlanda
		out1 = self.CohenSutherlandCode(xp,yp) 
		out2 = self.CohenSutherlandCode(xk,yk)
	
	#czesc wlasciwa
		while(True): 
			if((out1 | out2)== 0):  #w calosci wewnatrz prostokata
				accept = True
				break
			elif(out1 & out2): #w calosci po za prostokatem
				break
			else: #pozostale przypadki (przeciecie)
				
				if(out1 != 0 ):
					out = out1 
				else:
					out = out2
					
			#kolejne testy i obliczenia x,y
				if(out & 0b0001 ):#lewo
					x = self.xp
					y = yp+(yk-yp)*(x-xp)/(xk-xp)
				elif(out & 0b0010):#prawo
					x = self.xk
					y = yp+(yk-yp)*(x-xp)/(xk-xp)
				elif(out & 0b0100):#dol
					y = self.yp
					x = xp+(xk-xp)*(y-yp)/(yk-yp)
				elif(out & 0b1000): #gora
					y = self.yk
					x = (xk-xp)*(y-yp)/(yk-yp)
			#przygotowanie do kolejnej iteracji
				if(out == out1):
					xp = x
					yp = y
					out1 = self.CohenSutherlandCode(x, y)
				else:
					xk = x
					yk = y
					out2 = self.CohenSutherlandCode(x, y)
		return accept 
	
class LocalLine(): #klasa do obslugi linii
#------------ INCJALIZACJA ------------#
	def __init__(self,xp,yp,xk,yk):
		self.variables(xp,yp,xk,yk)
		self.setColorBlue()
		
	def variables(self,xp,yp,xk,yk): #zmienne
		#wspolrzedne kierunkowe
		#self.a = False
		#self.b = False
		self.xp = xp 
		self.yp = yp
		self.xk = xk
		self.yk = yk
	
	def flags(self,active): #wypisane flagi
		#self.f_active #czy jestem aktualnie rysowana
		#self.f_clikable #czy mozna we mnie kliknac
		self.f_marked = False # czy jestem zaznaczona
		self.f_moveend = False #czy ruszac koncem czy poczatkiem
		
#------------ Modyfikacja zmiennych ------------#
	def ChangeEndPoint(self,xk,yk):
		self.xk = xk
		self.yk = yk
		
	def moveByVector(self,x,y):
		self.xp = self.xp + x
		self.yp = self.yp + y
		
		self.xk = self.xk + x
		self.yk = self.yk + y
		
		self.calcAB()
	
	def ChangePoint(self,mx,my):
		if(self.f_moveend == True):
			self.ChangeEndPoint(mx,my)
		else:
			self.xp = mx
			self.yp = my
#------------ RYSOWANIE ------------#
	def draw(self): #rysuje pojedyncza linie
		glBegin(GL_LINES) 
		glColor3d(self.r,self.g,self.b)
		glVertex2f(self.xp, self.yp) 
		glVertex2f(self.xk, self.yk)
		glEnd()  
	
#------------ ZWRACANIE INFROMACJI ------------#
	def WhatAmILongTxt(self):
		return "Linia ("+str(self.xp)+","+str(self.yp)+") ("+str(self.xk)+","+str(self.yk)+")"
		
	def WhatAmITxt(self): 
		return "Linia"
		
	def WhatAmIInt(sefl):
		return 0
		
#------------ KOLORY ------------#
	def setColor(self,r,g,b):
		self.r = r
		self.g = g
		self.b = b
	
	def setColorRed(self): #ustwia kolor na czerwony, linia statyczna - tylko osie X,Y
		self.r = 1
		self.g = 0
		self.b = 0
		self.f_active = False
		self.f_clikable = False
		self.calcAB() 
	 
	def setColorBlue(self): #ustawia kolor na niebieski, linia aktualnie rysowana
		self.r = 0
		self.g = 0
		self.b = 1
		self.f_active = True
		self.f_clikable = True
	
	def setColorBlack(self): #ustawia kolor na czarny, linia statyczna
		#self.calcAB()
		self.r = 0
		self.g = 0
		self.b = 0
		self.f_active = False
		self.f_clikable = True
		self.calcAB()
	
	def setColorGreen(self): #ustawia kolor na zielony, czyli linia zaznaczona
		self.r = 0
		self.g = 1
		self.b = 0
	
#------------ ZAZNACZENIE ------------#
	def checkPoint(self,x,y,dx):
		if((self.xp - dx) <= x <= self.xp+dx )and(self.yp- dx <= y <= self.yp+dx):
			self.f_moveend = False
			return True
		elif(self.xk- dx <= x <= self.xk+dx )and(self.yk- dx <= y <= self.yk+dx):
			self.f_moveend = True
			return True
		else:
			return False
	
	def setMarked(self): #zaznacza linie
		self.setColorGreen()
		self.f_marked = True
	
	def setUnmarked(self): #odnacza linie
		self.setColorBlack()
		self.f_marked = False
	
	def AmIThere(self,xt,yt,dx): 
		#obliczenie brzegow
		ydpp = self.A*xt+(self.B-dx)
		ydpm = self.A*xt+(self.B+dx)
		
		#sprawdzenie czy trafiono we mnie
		if(ydpm <= yt <= ydpp): #czy na lini
			return True #bang - nie zyjesz :D
		elif(ydpm >= yt >= ydpp): #czy na lini 
			return True #bang - nie zyjesz :D
		return False #nie trafiono :(
		
	def AmIInside(self,xp,yp,xk,yk): 
		test = False
		
		if(xp <= self.xp <= xk): 
			if(yp <= self.yp <= yk):
				test = True
			elif(yp <= self.yk <= yk):
				test = True
		elif(xp <= self.xk <= xk): 
			
			if(yp <= self.yp <= yk):
				test = True
			elif(yp <= self.yk <= yk):
				test = True	
		return test
#------------ OBLICZENIOWE ------------#
	def calcAB(self): #oblicza A,B dla wzoru y=Ax+B
		if((self.xp-self.xk) != 0):
			self.A = (self.yp-self.yk) / (self.xp-self.xk)
			self.B = self.yk - (self.A*self.xk)
		elif(self.xp != 0):
			self.A = self.yp/self.xp
			self.B = 0
		elif(self.xk != 0):
			self.A = self.yk/self.xk
			self.B = 0
		else:
			self.A = 0
			self.B = 0
