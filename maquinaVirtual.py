from memoria import *
from Tkinter import *
from stack import *
from copy import *
master = Tk()

w = Canvas(master, width=1000, height=600)
w.pack()
lastFigura = ""
PReturn = Stack()
PQuads = Stack()
PDirs = Stack()
PMemorias = Stack()
inicioDirs = 6000
colores = {'rojo' : 'red', 'azul' : 'blue', 'verde' : 'green', 'negro' : 'black', 'morado' : 'purple', 'naranja' : 'orange', 'amarillo' : 'yellow'}
class MaquinaVirtual:
	def __init__(self):
		self.quads = []
		self.memoria = 0

	def ejecuta(self, quads, memoria):
		w.create_text(180, 20, text="PARTUM FIGURIS BY: PEDRO ESPARZA & JAVIER CRUZ")
		total = len(quads)
		i = 0
		while i<total:
			quadAux = quads[i]
			operador = quadAux[0]
			primero = quadAux[1]
			segundo = quadAux[2]
			tercero = quadAux[3]

			i = i+1
			if operador == '+':
				if primero >= inicioDirs:
					left = memoria.getValor(primero)
					left = memoria.getValor(left)
				else:
					left = memoria.getValor(primero)
				if segundo >= inicioDirs:
					right = memoria.getValor(segundo)
					right = memoria.getValor(right)
				else:
					right = memoria.getValor(segundo)
				memoria.insertar(left+right, tercero)
			if operador is '.':
				left = memoria.getValor(primero)
				memoria.insertar(left+segundo, tercero)
			if operador is '-':
				if primero >= inicioDirs:
					left = memoria.getValor(primero)
					left = memoria.getValor(left)
				else:
					left = memoria.getValor(primero)
				if segundo >= inicioDirs:
					right = memoria.getValor(segundo)
					right = memoria.getValor(right)
				else:
					right = memoria.getValor(segundo)
				memoria.insertar(left-right, tercero)
			if operador is '*':
				if primero >= inicioDirs:
					left = memoria.getValor(primero)
					left = memoria.getValor(left)
				else:
					left = memoria.getValor(primero)
				if segundo >= inicioDirs:
					right = memoria.getValor(segundo)
					right = memoria.getValor(right)
				else:
					right = memoria.getValor(segundo)
				memoria.insertar(left*right, tercero)
			if operador is '/':
				if primero >= inicioDirs:
					left = memoria.getValor(primero)
					left = memoria.getValor(left)
				else:
					left = memoria.getValor(primero)
				if segundo >= inicioDirs:
					right = memoria.getValor(segundo)
					right = memoria.getValor(right)
				else:
					right = memoria.getValor(segundo)
				if right == 0:
					print "Error! Division entre cero. Terminando ejecucion"
					sys.exit()
				memoria.insertar(left/right, tercero)
			if operador is '%':
				if primero >= inicioDirs:
					left = memoria.getValor(primero)
					left = memoria.getValor(left)
				else:
					left = memoria.getValor(primero)
				if segundo >= inicioDirs:
					right = memoria.getValor(segundo)
					right = memoria.getValor(right)
				else:
					right = memoria.getValor(segundo)
				memoria.insertar(left%right, tercero)
			if operador is '<':
				if primero >= inicioDirs:
					left = memoria.getValor(primero)
					left = memoria.getValor(left)
				else:
					left = memoria.getValor(primero)
				if segundo >= inicioDirs:
					right = memoria.getValor(segundo)
					right = memoria.getValor(right)
				else:
					right = memoria.getValor(segundo)
				memoria.insertar(left<right, tercero)
			if operador == '>':
				if primero >= inicioDirs:
					left = memoria.getValor(primero)
					left = memoria.getValor(left)
				else:
					left = memoria.getValor(primero)
				if segundo >= inicioDirs:
					right = memoria.getValor(segundo)
					right = memoria.getValor(right)
				else:
					right = memoria.getValor(segundo)
				memoria.insertar(left>right, tercero)
			if operador == "<=":
				if primero >= inicioDirs:
					left = memoria.getValor(primero)
					left = memoria.getValor(left)
				else:
					left = memoria.getValor(primero)
				if segundo >= inicioDirs:
					right = memoria.getValor(segundo)
					right = memoria.getValor(right)
				else:
					right = memoria.getValor(segundo)
				memoria.insertar(left<=right, tercero)
			if operador == ">=":
				if primero >= inicioDirs:
					left = memoria.getValor(primero)
					left = memoria.getValor(left)
				else:
					left = memoria.getValor(primero)
				if segundo >= inicioDirs:
					right = memoria.getValor(segundo)
					right = memoria.getValor(right)
				else:
					right = memoria.getValor(segundo)
				memoria.insertar(left>=right, tercero)
			if operador == "==":
				if primero >= inicioDirs:
					left = memoria.getValor(primero)
					left = memoria.getValor(left)
				else:
					left = memoria.getValor(primero)
				if segundo >= inicioDirs:
					right = memoria.getValor(segundo)
					right = memoria.getValor(right)
				else:
					right = memoria.getValor(segundo)
				memoria.insertar(left==right, tercero)
			if operador == "&&":
				left = memoria.getValor(primero)
				right = memoria.getValor(segundo)
				memoria.insertar(left&right, tercero)
			if operador == "||":
				left = memoria.getValor(primero)
				right = memoria.getValor(segundo)
				memoria.insertar(left|right, tercero)
			if operador is '=':
				if primero >= inicioDirs:
					left = memoria.getValor(primero)
					left = memoria.getValor(left)
				else:
					left = memoria.getValor(primero)
				if tercero >= inicioDirs:
					tercero = memoria.getValor(tercero)
				memoria.insertar(left, tercero)
			if operador is 'meter':
				memoria.insertar(primero, tercero)
			if operador is 'Goto':
				i = tercero
			if operador is 'GotoF':
				exp = memoria.getValor(primero)
				q = tercero
				if exp == 'falso':
					i = q
				if not exp:
					i = q
			if operador is 'GotoV':
				exp = memoria.getValor(primero)
				q = tercero
				if exp:
					i = q 
			if operador is 'ERA':
				size = segundo
			if operador is 'GOSUB':
				PQuads.push(i)
				PReturn.push(i)
				memoriaAux = deepcopy(memoria)
				PMemorias.push(memoria)
				memoria = deepcopy(memoriaAux)
				i = segundo
			if operador is 'REGRESA':
				PDirs.push(tercero)
			if operador is 'REGRESAF':
				print memoria.getValor(tercero)
				print "Ejecucion terminada"
			if operador is 'END':
				if PDirs.size() is not 0:
					ultimoReturn = PDirs.pop()
					valor = memoria.getValor(ultimoReturn)
					memoria = deepcopy(PMemorias.pop())
					memoria.insertar(valor, ultimoReturn)
				else:
					memoria = deepcopy(PMemorias.pop())

				i = PQuads.pop()
			if operador is 'print':
				if tercero >= inicioDirs:
					valor = memoria.getValor(tercero)
					valor = memoria.getValor(valor)
				else:
					valor = memoria.getValor(tercero)
				print valor
			if operador is 'pedir':
				if tercero >= inicioDirs:
					tercero = memoria.getValor(tercero)
				x = raw_input('Cual es el valor de ' + (primero) + '?  ')
				if tercero <1999:
					x = int(x)
				else:
					x = float(x)
				memoria.insertar(x, tercero)
			if operador is 'PARAMETER':
				argumento = memoria.getValor(primero)
				memoria.insertar(argumento, segundo)
			if operador is "l":
				lista = primero
				x1 = lista[0]
				y1 = lista[1]
				x2 = lista[2]
				y2 = lista[3]
				if x1 >= inicioDirs:
					x1 = memoria.getValor(x1)
				if x2 >= inicioDirs:
					x2 = memoria.getValor(x2)
				if y1 >= inicioDirs:
					y1 = memoria.getValor(y1)
				if y2 >= inicioDirs:
					y2 = memoria.getValor(y2)
				x1 = memoria.getValor(x1)
				y1 = memoria.getValor(y1)
				x2 = memoria.getValor(x2)
				y2 = memoria.getValor(y2)
				x = w.create_line(x1, y1,x2, y2)
			if operador is "verif":
				numero = memoria.getValor(segundo)
				limite = tercero
				if numero > limite | numero < 0:
					print "Error en el indice del arreglo"
					sys.exit()
			if operador is 'a':
				lastFigura = "arco"
			if operador is 'r':
				lastFigura = "cuadro"
			if operador is 't':
				lastFigura = "texto"
			if operador is 'c':
				lastFigura = "circulo"
			if operador is 't':
				lastFigura = "triangulo"
			if operador is 'k':
				if lastFigura == "cuadro":
					lista = segundo
					ancho = lista[0]
					alto = lista[1]
					xpos = lista[2]
					ypos = lista[3]
					if ancho >= inicioDirs:
						ancho = memoria.getValor(ancho)
					if alto >= inicioDirs:
						alto = memoria.getValor(alto)
					if xpos >= inicioDirs:
						xpos = memoria.getValor(xpos)
					if ypos >= inicioDirs:
						ypos = memoria.getValor(ypos)
					xpos = memoria.getValor(xpos)
					ypos = memoria.getValor(ypos)
					alto = memoria.getValor(alto)
					ancho = memoria.getValor(ancho)
					color = tercero;
					color = colores[color]
					cuadrado = w.create_rectangle(xpos, ypos, alto, ancho, fill=color)
				if lastFigura == "circulo":
					lista = segundo
					x2 = lista[0]
					y2 = lista[1]
					x1 = lista[2]
					y1 = lista[3]
					if x1 >= inicioDirs:
						x1 = memoria.getValor(x1)
					if x2 >= inicioDirs:
						x2 = memoria.getValor(x2)
					if y1 >= inicioDirs:
						y1 = memoria.getValor(y1)
					if y2 >= inicioDirs:
						y2 = memoria.getValor(y2)
					x1 = memoria.getValor(x1)
					y1 = memoria.getValor(y1)
					x2 = memoria.getValor(x2)
					y2 = memoria.getValor(y2)
					color = tercero;
					color = colores[color]
					cuadrado = w.create_oval(x1, y1, y2, x2, fill=color)
				if lastFigura == "triangulo":
					lista = segundo
					color = tercero
					color = colores[color]
					x1 = lista[0]
					x3 = lista[4]
					y3 = lista[5]
					y1 = lista[1]
					x2 = lista[2]
					y2 = lista[3]
					if x1 >= inicioDirs:
						x1 = memoria.getValor(x1)
					if x2 >= inicioDirs:
						x2 = memoria.getValor(x2)
					if x3 >= inicioDirs:
						x3 = memoria.getValor(x3)
					if y1 >= inicioDirs:
						y1 = memoria.getValor(y1)
					if y2 >= inicioDirs:
						y2 = memoria.getValor(y2)
					if y3 >= inicioDirs:
						y3 = memoria.getValor(y3)
					x1 = memoria.getValor(x1)
					x2 = memoria.getValor(x2)
					x3 = memoria.getValor(x3)
					y1 = memoria.getValor(y1)
					y2 = memoria.getValor(y2)
					y3 = memoria.getValor(y3)
					tirnagulo = w.create_polygon((x1, y1),(x2, y2),(x3,y3), fill=color)
				if lastFigura == "arco":
					lista = segundo
					ancho = lista[0]
					alto = lista[1]
					xpos = lista[2]
					ypos = lista[3]
					if ancho >= inicioDirs:
						ancho = memoria.getValor(ancho)
					if alto >= inicioDirs:
						alto = memoria.getValor(alto)
					if xpos >= inicioDirs:
						xpos = memoria.getValor(xpos)
					if ypos >= inicioDirs:
						ypos = memoria.getValor(ypos)
					xpos = memoria.getValor(xpos)
					ypos = memoria.getValor(ypos)
					alto = memoria.getValor(alto)
					ancho = memoria.getValor(ancho)
					color = tercero
					color = colores[color]
					arco = w.create_arc(xpos, ypos, alto, ancho, outline=color, extent=90, style=ARC,)
		mainloop()
