import os
inicioEnteros = 1000
limiteEnteros = 1999
limiteDobles = 2999
limiteBoleanos = 3999
limiteTemporales = 4999
limiteConstantes = 5999
limiteDirecciones = 6999
class Memoria:
	def __init__(self):
		self.enteros = {}
		self.dobles = {}
		self.boleanos = {}
		self.constantes = {}
		self.temporales = {}
		self.direcciones = {}
	def insertar(self, valor, direccion):
		if direccion >= inicioEnteros and direccion < limiteEnteros:
			self.enteros[direccion] = valor
		if direccion < limiteDobles:
			self.dobles[direccion] = valor
		if direccion < limiteBoleanos:
			self.boleanos[direccion] = valor
		if direccion < limiteTemporales:
			self.temporales[direccion] = valor
		if direccion < limiteConstantes:
			self.constantes[direccion] = valor
		if direccion < limiteDirecciones:
			self.direcciones[direccion] = valor

	def getValor(self, direccion):
		if direccion >=inicioEnteros and direccion < limiteEnteros:
			if self.enteros.get(direccion) is not None:
				return self.enteros[direccion]
			else:
				print "Error, variable no inicializada"
				os._exit(1)
		if direccion < limiteDobles:
			if self.dobles.get(direccion) is not None:
				return self.dobles[direccion]
			else:
				print "Error, variable no inicializada"
				os._exit(1)
		if direccion < limiteBoleanos:
			if self.boleanos.get(direccion) is not None:
				return self.boleanos[direccion]
			else:
				print "Error, variable no inicializada"
				os._exit(1)	
		if direccion < limiteTemporales:
			if self.temporales.get(direccion) is not None:
				return self.temporales[direccion]
			else:
				print "Error, variable no inicializada"
				os._exit(1)
		if direccion < limiteConstantes:
			if self.constantes.get(direccion) is not None:
				return self.constantes[direccion]
			else:
				print "Error, variable no inicializada"
				os._exit(1)
		if direccion < limiteDirecciones:
			if self.direcciones.get(direccion) is not None:
				return self.direcciones[direccion]
			else:
				print "Error, variable no inicializada"
				os._exit(1)



