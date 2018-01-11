# coding=utf-8
#------------------------------
# scanner.py
#------------------------------
import ply.yacc as yacc
import sys
from sets import Set
import ply.lex as lex
from cuboSemantico import *
from stack import *
from memoria import *
from maquinaVirtual import *
#lista de palabras reservadas
reserved = {
	'funcion' : 'FUNCION',
	'principal' : 'PRINCIPAL',
	'regresa' : 'REGRESA',
	'si' : 'SI',
	'sino' : 'SINO',
	'mientras' : 'MIENTRAS',
	'escribir' : 'ESCRIBIR',
	'escribirS' : 'ESCRIBIRS',
	'crearArco' : 'CREARARCO',
	'crearCuadro' : 'CREARCUADRO',
	'crearTriangulo' : 'CREARTRIANGULO',
	'crearCirculo' : 'CREARCIRCULO',
	'crearLinea' : 'CREARLINEA',
	'pedir' : 'PEDIR',
	'rojo' : 'ROJO',
	'verde' : 'VERDE',
	'azul' : 'AZUL',
	'morado' : 'MORADO',
	'naranja' : 'NARANJA',
	'negro' : 'NEGRO',
	'amarillo' : 'AMARILLO',
	'entero' : 'ENTERO_RW',
	'doble' : 'DOBLE_RW',
	'verdadero' : 'VERDADERO',
	'falso' : 'FALSO',
	'boleano' : 'BOLEANO_RW',
	'void' : 'VOID_RW'
}

# Lista de tokens
tokens = [
	'PARENTESIS_IZQ',
	'PARENTESIS_DER',
	'CORCHETE_IZQ',
	'CORCHETE_DER',
	'LLAVE_IZQ',
	'LLAVE_DER',
	'COMA',
	'PUNTO_COMA',
	'AND',
	'OR',
	'MENOS',
	'MAS',
	'ENTRE',
	'POR',
	'MOD',
	'IGUAL',
	'MENOR_QUE',
	'MAYOR_QUE',
	'IGUAL_IGUAL',
	'MENOR_IGUAL',
	'MAYOR_IGUAL',
	'DIFERENTE_DE',
	'DOBLE',
	'ENTERO',	
	'ID',
	'STRING'] + list(reserved.values())

# Expresiones regulares simples
t_PARENTESIS_IZQ = r'\('
t_PARENTESIS_DER = r'\)'
t_CORCHETE_IZQ	= r'\['
t_CORCHETE_DER	= r'\]'
t_LLAVE_IZQ	= r'{'
t_LLAVE_DER	= r'}'
t_COMA 		= r','
t_PUNTO_COMA	= r';'
t_AND		= r'&&'
t_OR		= r'\|\|'
t_MENOS		= r'-'
t_MAS		= r'\+'
t_ENTRE		= r'/'
t_POR		= r'\*'
t_MOD		= r'%'
t_IGUAL 	= r'='
t_MENOR_QUE	= r'<'
t_MAYOR_QUE 	= r'>'
t_IGUAL_IGUAL	= r'=='
t_MENOR_IGUAL	= r'<='
t_MAYOR_IGUAL	= r'>='
t_DIFERENTE_DE 	= r'!='

def t_DOBLE(t):
	r'(-)?\d+\.\d+'
	t.value = float(t.value)
	return t

def t_ENTERO(t):
	r'(-)?\d+'
	t.value = int(t.value)
	return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')    #Revisar palabras reservadas
    return t

def t_STRING(t):
	r'".*"'
	t.value = str(t.value)
	return t

# Numeros de linea
def t_newline(t):
	r'\n+'
	t.lexer.lineno += len(t.value)

#Ignorar todo lo demás
t_ignore  = ' \t'

#Manejar errores
def t_error(t):
    print('''Caracter no valido '%s''' % t.value[0])
    t.lexer.skip(1)

# Construir lexer
lexer = lex.lex()

#Variables
memoria = Memoria() #La memoria del compilador
maquina = MaquinaVirtual() #La maquina virtual del compilador
quads = [] #lista de cuadruplos
POper = Stack() #pila de operadores
PExps = Stack() #pila de expresiones
PTipos = Stack() # pila de tipos
PSaltos = Stack() # pila de saltos
PArreglos = Stack() # pila de ids de arreglos
PTArreglos = Stack() #pila de tioos de arreglos
PEra = Stack() #pula de relleno de ERA
lastOper =  [] # ultimo operador
TablaVariables = {} #diccionario como tabla de variables
TablaVariables['global'] = {} #crear global en el diccionario de tabla de variables
ultimoTipo = [] # ultimo tipo
ultimoTipoFunc = [] # ultimo tipo de funcion
global scope # scope de cierta variable
scope = ['global'] #global como primer scope
directorioFunciones = {} #diccionario como dir procedures
global expresion #expresion para los prints
expresion = "" #expresion inicia vacia
global k #K de parametros
k = 0 #K inicia en cero
global parametros #parametros de funciones
parametros = [] #parametros inicia vacio
global direcciones #Para match de parametros y argumento
direcciones = [] #inicia vacio
global varDim #variable para checar si una variable fue arreglo
inicioInt = 1000 #dirVirutal de inicio de los entero
inicioDoble = 2000 #dirVirtual de inicio de los dobles
inicioBoleano = 3000 #dirVirtual de inicio de los boleanos
inicioTemps = 4000 #dirVirutal de inicio de los temporales
inicioCons = 5000 # dir Virtual de inicio de las constantes
inicioDirs = 6000 #dir Virtual de inicio de las direcciones de direcciones
limiteEntero = 1999 # dirVirutal limite de enteros
limiteDoble = 2999 # dirVirutal limite de dobles
limiteBoleano = 3999 # dirVirutal limite de boleanos
limiteTemps = 4999 # dirVirutal limite de temporales
limiteCons = 5999 # dirVirutal limite de constantes
limiteDirs = 6999 # dirVirutal limite de direcciones de direcciones
global contEntero #contador de enteros
contEntero = 1000 #incia en 1000
global contDoble # contador de dobles
contDoble = 2000 #incia en 2000
global contBoleano #contador de boleanos
contBoleano = 3000 #inicia en 3000
global contTemps #contador de temporadores
contTemps = 4000 #inicia en 4000
global contCons #contador de constantes
contCons = 5000 #inicia en 5000
global funcEntero #enteros de una funcion
funcEntero = 0 #inician en cero
global funcDoble #dobles de una funcion
funcDoble = 0 #inician en cero
global funcBool #boleanos de una funcion
funcBool = 0  #inician en cero
global funcTemp #temporales de una funcion
funcTemp = 0  #inician en cero
global funcCons #constantes de una funcion
funcCons = 0  #inician en cero
global contDirs #contador de direcciones
contDirs = 6000 #inicia en 6000
global funcDirs #direcciones en una funcion
funcDirs = 0 #inician en cero
# Gramatica
def p_programa(p):
	'''programa : empieza vars funciones principal finalCodigo'''
	p[0] = 'PROGRAM COMPILED'

def p_vars(p):
	'''vars : tipo ID agregarVar s1 s2 PUNTO_COMA vars
		| '''

def p_s1(p):
	'''s1 : CORCHETE_IZQ ENTERO CORCHETE_DER siDim
	      | '''

def p_s2(p):
	'''s2 : COMA ID agregarVar s1 s2
	      | '''

def p_funciones(p):
	'''funciones : borrarTodo FUNCION tipoFun ID agregarFunc PARENTESIS_IZQ parametros PARENTESIS_DER bloqueFun checaSize actualSize funciones
		     | '''

def p_tipo(p):
	''' tipo : DOBLE_RW
		 | ENTERO_RW
		 | BOLEANO_RW'''
	p[0] = p[1]
	ultimoTipo.append(p[0])

def p_tipoFun(p):
	'''tipoFun : DOBLE_RW
		   | ENTERO_RW
		   | BOLEANO_RW
		   | VOID_RW'''
	p[0] = p[1]
	ultimoTipoFunc.append(p[0])

def p_principal(p):
	'principal : PRINCIPAL to_func_principal empiezaP bloqueP'

def p_parametros(p):
	'''parametros : tipo ID to_func_param s3
			| '''

def p_s3(p):
	'''s3 : COMA tipo ID to_func_param s1 s3
	      | '''

def p_bloqueP(p):
	'bloqueP : LLAVE_IZQ cuerpoP LLAVE_DER'

def p_bloqueFun(p):
	'bloqueFun : LLAVE_IZQ cuerpoFun LLAVE_DER'

def p_cuerpoFun(p):
	'cuerpoFun : vars subirFuncion estatuto s5 finFuncion'

def p_s5(p):
	'''s5 : REGRESA exp PUNTO_COMA checaREGRESA
	      | '''

def p_cuerpoP(p):
	'cuerpoP : vars estatuto REGRESA exp PUNTO_COMA'

def p_bloque(p):
	'bloque : LLAVE_IZQ cuerpo LLAVE_DER'

def p_cuerpo(p):
	'''cuerpo : estatuto '''

def p_estatuto(p):
	'''estatuto : asignacion estatuto
		    | condicion estatuto
		    | ciclo estatuto
		    | escribir estatuto
		    | escribirS estatuto
		    | pedirValor estatuto
		    | llamarVoid estatuto
		    | predefinido estatuto
		    | '''

def p_asignacion(p):
	'asignacion : ID checa_existe idAPila s20 IGUAL operPila expresion checaasigna PUNTO_COMA'

def p_pedirValor(p):
	'pedirValor : PEDIR PARENTESIS_IZQ ID checa_existe PARENTESIS_DER PUNTO_COMA irPedir'

def p_condicion(p):
	'condicion : SI PARENTESIS_IZQ expresion PARENTESIS_DER checaExp bloque s6'

def p_s6(p):
	'''s6 : SINO entroElse bloque finIFELSE
	    | finIF'''

def p_ciclo(p):
	'ciclo : MIENTRAS subirWhile PARENTESIS_IZQ expresion checaExp PARENTESIS_DER bloque subeWhile'

def p_escribir(p):
	'escribir : ESCRIBIR PARENTESIS_IZQ exp PARENTESIS_DER printear PUNTO_COMA'

def p_escribirS(p):
	'escribirS : ESCRIBIRS PARENTESIS_IZQ STRING mostrar_expresion PARENTESIS_DER PUNTO_COMA'

def p_llamarFuncion(p):
	'llamarFuncion : ID checaFuncion PARENTESIS_IZQ args PARENTESIS_DER checaResto GOSUB funcionPila'

def p_llamarVoid(p):
	'llamarVoid : ID checaFuncion PARENTESIS_IZQ args PARENTESIS_DER checaResto GOSUB PUNTO_COMA'

def p_args(p):
	'''args : exp checaArg s9
		| '''

def p_s9(p):
	'''s9 : COMA masArgs args
	      | '''

def p_predefinido(p):
	'''predefinido : crearArco
			| crearCuadro
			| crearLinea
			| crearCirculo
			| crearTriangulo'''

def p_expresion(p):
	'expresion : comparacion s10'

def p_s10(p):
	'''s10 : OR operPila s11
		| AND operPila s11
		| '''

def p_s11(p):
	's11 : expresion resolvANDOR '

def p_comparacion(p):
	'comparacion : exp s12'

def p_s12(p):
	'''s12 : operador operPila exp resolvRel
		| '''

def p_exp(p):
	'exp : termino resolvBasic s13'

def p_s13(p):
	'''s13 : MAS operPila s14
		| MENOS operPila s14
		| '''

def p_s14(p):
	's14 : exp'

def p_termino(p):
	'termino : factor resolvComp s15'

def p_s15(p):
	'''s15 : ENTRE operPila s16
		| POR operPila s16
		| MOD operPila s16
		| '''

def p_s16(p):
	's16 : termino'

def p_factor(p):
	'''factor : llamarFuncion
		  | s17 
		  | ENTERO enteroPila
		  | DOBLE doblePila
		  | VERDADERO boolPila
		  | FALSO boolPila
		  | PARENTESIS_IZQ operPila exp PARENTESIS_DER sacaPila'''

def p_s17(p):
    's17 : ID checa_existe varPila s20'

def p_operador(p):
    '''operador : MENOR_QUE
            | MAYOR_QUE
            | IGUAL_IGUAL
            | MENOR_IGUAL
            | MAYOR_IGUAL
            | DIFERENTE_DE'''
    p[0] = p[1]

def p_crearArco (p):
    'crearArco : CREARARCO nuevo_objeto_arco quadFigura baseFigura'

def p_crearCirculo (p):
    'crearCirculo : CREARCIRCULO nuevo_objeto_circulo quadFigura baseFigura'

def p_crearCuadro (p):
	'crearCuadro : CREARCUADRO nuevo_objeto_cuadro quadFigura baseFigura'

def p_crearTriangulo (p): 
    'crearTriangulo : CREARTRIANGULO nuevo_objeto_trian quadFigura baseFiguraTriangulo'

def p_crearLinea(p):
    'crearLinea : CREARLINEA nuevo_objeto_linea PARENTESIS_IZQ ID agregarVar COMA exp COMA exp COMA exp COMA exp PARENTESIS_DER quadLinea PUNTO_COMA'

def p_baseFigura(p):
    'baseFigura : PARENTESIS_IZQ ID agregarVar COMA exp COMA exp COMA exp COMA exp COMA color PARENTESIS_DER restoCrear PUNTO_COMA'

def p_baseFiguraTriangulo(p):
    'baseFiguraTriangulo : PARENTESIS_IZQ ID agregarVar COMA exp COMA exp COMA exp COMA exp COMA exp COMA exp COMA color PARENTESIS_DER restoCrearTriangulo PUNTO_COMA'

def p_color(p):
    '''color : ROJO
        | VERDE
        | AZUL
        | MORADO
        | NARANJA
        | NEGRO
        | AMARILLO'''
    p[0] = p[1]

def p_s20(p):
	'''s20 : CORCHETE_IZQ usaArr exp CORCHETE_DER usaArr1
		| '''

#Puntos neuralgicos

#Recibe: p[-4] como una variable
#Regresa: No aplica
#Cuadruplos: cuadruplo 'pedir'
#Donde se usa: pedirValor
#Que hace: crea un cadruplo para pedir un valor usuario
def p_irPedir(p):
	#Crear cuadruplo para pedir un valor al usuario
	'''irPedir : '''
	var = p[-4]
	esteScope = TablaVariables[scope[len(scope)-1]]
	direccion = esteScope[var]['dirVirtual']
	quadAux = ['pedir', var, 0 , direccion]
	quads.append(quadAux)

#Recibe: No aplica
#Regresa: No aplica
#Cuadruplos: cuadruplo 'print'
#Donde se usa: escribir
#Que hace: crea un cadruplo para
def p_printear(p):
	#Crear cuadruplo para desplegar un valor 
	'''printear :'''
	var = PExps.pop()
	quadAux = ['print', 0, 0, var]
	quads.append(quadAux)

#Recibe: No aplica
#Regresa: No aplica
#Cuadruplos: cuadruplo 'Goto'
#Donde se usa: programa
#Que hace: crea un cadruplo para ir al main
def p_empieza(p):
	#Crear el cuadruplo para ir al main
	'''empieza :'''
	quadAux = ['Goto', 0, 0, 0]
	quads.append(quadAux)

#Recibe: quad[0] como cuadruplo Aux
#Regresa: No aplica
#Cuadruplos: No aplica
#Donde se usa: principal
#Que hace: Rellena el cuadruplo que baja al main
def p_empiezaP(p):
	#Rellenar el cuadruplo que baja al main
	'''empiezaP :'''
	quadAux = quads[0]
	quadAux[3] = len(quads)
	quads[0] = quadAux

#Recibe: PTipos.pop() como tipoFinal y PExps.pop() como Expresion
#Regresa: No aplica
#Cuadruplos: cuadruplo 'REGRESAF'
#Donde se usa: programa
#Que hace: genera el cuádruplo obligatorio de final de codigo
def p_finalCodigo(p):
	'''finalCodigo :'''
	#para el ultimo REGRESA obligatorio
	tipoFinal = PTipos.pop()
	numeroFinal = PExps.pop()
	quadAux = ['REGRESAF', 0, 0, numeroFinal]
	quads.append(quadAux)

#Recibe: p[-1] como var
#Regresa: No aplica
#Cuadruplos: No aplica
#Donde se usa: vars, s2, crearLinea, baseFigura, baseFiguraTriangulo
#Que hace: agrega las variables a la tabla de variables
def p_agregarVar(p):
	'''agregarVar :'''
	var = p[-1]
	#para checar si es arreglo
	global varDim
	varDim = var
	esteScope = TablaVariables[scope[len(scope)-1]]
	if var not in esteScope:#si no esta en el scope
		esteScope[var] = {}#los atributos de la variable en un diccionario
		esteScope[var]['tipo'] = ultimoTipo[len(ultimoTipo)-1] #agrego su tipo
		#si es entero,doble o boleano debo agregar su dirVirtual
		tipo = esteScope[var]['tipo']
		if tipo == 'entero':
			global contEntero
			esteScope[var]['dirVirtual'] = contEntero
			contEntero = contEntero+1
			if contEntero > limiteEntero:
				print "Linea {0}: Se acabo la memoria".format(lexer.lineno)
				sys.exit()
			global funcEntero
			funcEntero = funcEntero +1
		if tipo == 'doble':
			global contDoble
			esteScope[var]['dirVirtual'] = contDoble
			contDoble = contDoble+1
			if contDoble > limiteDoble:
				print "Linea {0}: Se acabo la memoria".format(lexer.lineno)
				sys.exit()
			global funcDoble
			funcDoble = funcDoble +1
		if tipo == 'boleano':
			global contBoleano
			esteScope[var]['dirVirtual'] = contBoleano
			contBoleano = contBoleano+1
			if contBoleano > contBoleano:
				print "Linea {0}: Se acabo la memoria".format(lexer.lineno)
				sys.exit()
			global funcBool
			funcBool = funcBool +1
		#por ahora su dimension es 0
		esteScope[var]['dim'] = 0
	else:
		print "Linea {0}: Variable previamente declarada".format(lexer.lineno)
		sys.exit()

#Recibe: p[-2] como n
#Regresa: No aplica
#Cuadruplos: No aplica
#Donde se usa: s1
#Que hace: agrega las variables dimensionadas a la tabla de variables
def p_siDim(p):
	'''siDim :'''
	#la variable si fue arreglo
	n = p[-2]
	esteScope = TablaVariables[scope[len(scope)-1]]
	esteScope[varDim]['dim'] = n #n como dimension
	#si es entero o doble debo inabilitar las siguientes n-1 dirVirtuales
	if esteScope[varDim]['dim'] > 0:
		global contEntero
		contEntero = contEntero + (n-1)
		if contEntero > limiteEntero:
			print "Linea {0}: Se acabo la memoria".format(lexer.lineno)
			sys.exit()
		global funcEntero
		funcEntero = funcEntero + (n-1)
	if esteScope[varDim]['dim'] > 0:
		global contDoble 
		contDoble = contDoble + (n-1)
		if contDoble > limiteDoble:
			print "Linea {0}: Se acabo la memoria".format(lexer.lineno)
			sys.exit()
		global funcDoble
		funcDoble = funcDoble + (n-1)
	if esteScope[varDim]['dim'] > 0:
		global contBoleano 
		contBoleano = contBoleano + (n-1)
		if contBoleano > limiteBoleano:
			print "Linea {0}: Se acabo la memoria".format(lexer.lineno)
			sys.exit()
		global funcBool
		funcBool = funcBool + (n-1)

#Recibe: p[-7] como funcion
#Regresa: No aplica
#Cuadruplos: No aplica
#Donde se usa: funciones
#Que hace: rellenar el cuadruplo de ERA con el tamano de la funcion
def p_actualSize(p):
	'''actualSize :'''
	#si hay recursion,no se el tamaño de la funcion hasta recorrerla toda por lo que debo actualizarla
	# una vez que salga de la funcion
	funcion = p[-7]
	while not PEra.isEmpty():
		lugar = PEra.pop()
		quadAux = quads[lugar]
		quadAux[2] = directorioFunciones[funcion]['size']
		quads[lugar] = quadAux

#Recibe: No aplica
#Regresa: No aplica
#Cuadruplos: No aplica
#Donde se usa: funciones
#Que hace: reiniciar variables con valor de cero
def p_borrarTodo(p):
	'''borrarTodo :'''
	#borrar los contadores de vairbales de una funcionn para el size
	global funcDoble
	funcDoble = 0
	global funcEntero
	funcEntero = 0
	global funcBool
	funcBool
	global funcTemp
	funcTemp = 0
	global funcCons
	funcCons = 0
	global funcDirs
	funcDirs = 0

#Recibe: p[-6] como funcion
#Regresa: No aplica
#Cuadruplos: No aplica
#Donde se usa: funciones
#Que hace: crea el tamano de las variables de funcion
def p_checaSize(p):
	'''checaSize :'''
	#crear el size de variables de la funcion
	funcion = p[-6]
	global funcDoble
	global funcEntero
	global funcBool
	global funcTemp
	global funcCons
	directorioFunciones[funcion]['size'] = [funcEntero, funcDoble, funcBool, funcTemp, funcCons]

#Recibe: p[-1] como funcion
#Regresa: No aplica
#Cuadruplos: No aplica
#Donde se usa: funciones
#Que hace: agrega la funcion a la tabla de variables
def p_agregarFunc(p):
	'''agregarFunc :'''
	#meter la funcion a su tabla
	funcion = p[-1]
	if funcion not in scope and funcion not in TablaVariables['global']: #que no exista, que no sea variable etc
		scope.append(p[-1])#indicar el scope al que entre
		TablaVariables[funcion] = {} #agregar la funcname a la TablaVariables
		directorioFunciones[funcion] = {}
		func = directorioFunciones[funcion] #creo un diccionario para guardar los atirbutos de la funcion
		func['tipo'] = p[-2] #inserto el tipo
		func['param'] = [] #  lista para parametros
		func['quad'] = 0 #quad que es cero por mientras
		func['size'] = [] #lista para el tamaño
		func['direcciones'] = []
		func['return'] = 0
	else:
		print "Linea {0}: Procedimiento previamente delcarado".format(lexer.lineno)
		sys.exit()

#Recibe: No aplica
#Regresa: No aplica
#Cuadruplos: No aplica
#Donde se usa: principal
#Que hace: inicializacion de scope y tabla de variables en el main
def p_to_func_principal(p):
	'''to_func_principal :'''
	#cuando entro al main 
	scope.append(p[-1])#ultimo scope es main
	TablaVariables[p[-1]] = {} #creo la TablaVariables de principal

#Recibe: p[-1] como funcion, p[-2] como tipoo
#Regresa: No aplica
#Cuadruplos: No aplica
#Donde se usa: parametros, s3
#Que hace: cuenta y valida los parametros de una funcion
def p_to_func_param(p):
	'''to_func_param :'''
	#meter los parametros a su funcion
	var = p[-1]
	tipoo = p[-2]
	esteScope = TablaVariables[scope[len(scope)-1]]
	directorioFunciones[scope[len(scope)-1]]['param'].append(tipoo)
	#si la variable no fue previamente declarada 
	if var not in TablaVariables[scope[len(scope)-1]]:
		esteScope[var] = {}
		esteScope[var]['tipo'] = tipoo
		esteScope[var]['dim'] = 0
		#dependiendo del tipo, agregar 1 al contador de variables en funciones
		if tipoo == 'entero':
			global funcEntero
			funcEntero = funcEntero + 1
			global contEntero
			esteScope[var]['dirVirtual'] = contEntero
			contEntero = contEntero + 1
			if contEntero > limiteEntero:
				print "Linea {0}: Se acabo la memoria".format(lexer.lineno)
				sys.exit()
		if tipoo == 'doble':
			global funcDoble
			funcDoble = funcDoble + 1
			global contDoble
			esteScope[var]['dirVirtual'] = contDoble
			contDoble = contDoble + 1
			if contDoble > limiteDoble:
				print "Linea {0}: Se acabo la memoria".format(lexer.lineno)
				sys.exit()
		if tipoo == 'boleano':
			global funcBool
			funcBool = funcBool + 1
			global contBoleano
			esteScope[var]['dirVirtual'] = contBoleano
			contBoleano = contBoleano+1
			if contBoleano > contBoleano:
				print "Linea {0}: Se acabo la memoria".format(lexer.lineno)
				sys.exit()
		directorioFunciones[scope[len(scope)-1]]['direcciones'].append(esteScope[var]['dirVirtual'])
	else:
		print "Linea {0}: Procedimiento previamente declarado".format(lexer.lineno)
		sys.exit()

#Recibe: No aplica
#Regresa: No aplica
#Cuadruplos: No aplica
#Donde se usa: cuerpoFun
#Que hace: conocer el quad al llamar una funcion
def p_subirFuncion(p):
	'''subirFuncion :'''
	#conocer el quad a donde dirigirse al llamar una funcion
	directorioFunciones[scope[len(scope)-1]]['quad'] = len(quads)

#Recibe: No aplica
#Regresa: No aplica
#Cuadruplos: 'END'
#Donde se usa: cuerpoFun
#Que hace: crea el quad para terminar la funcion
def p_finFuncion(p):
	'''finFuncion :'''
	#crea el quad del end de funcion
	quadAux = ['END', 0, 0, 0]
	quads.append(quadAux)

#Recibe: PExps.pop() como valorR, Ptipos.pop() como tipoR
#Regresa: No aplica
#Cuadruplos: No aplica
#Donde se usa: s5
#Que hace: valida que el regresa sea lo que se espera
def p_checaREGRESA(p):
	'''checaREGRESA :'''
	#checa que el REGRESA sea del tipo
	valorR = PExps.pop()
	tipoR = PTipos.pop()
	if directorioFunciones[scope[len(scope)-1]]['tipo'] != 'void': #no debe ser void
		if	directorioFunciones[scope[len(scope)-1]]['tipo'] != tipoR:#tipos iguales
			print "Linea {0}: Error en el regresa".format(lexer.lineno)
			sys.exit()
		else:
			global contTemps
			quadAux = ['REGRESA', 0, 0, contTemps-1]
			directorioFunciones[scope[len(scope)-1]]['regresa'] = contTemps-1
			quads.append(quadAux)
	else:#si es void lo ignoro
		print "Linea {0}: No debe haber regresa".format(lexer.lineno)
		sys.exit()

#Recibe: p[-2] como var
#Regresa: No aplica
#Cuadruplos: No aplica
#Donde se usa: asignacion
#Que hace: mete la direccion del id a la pila de Exp y su tipo a la de tipos
def p_idAPila(p):
	'''idAPila :'''
	#meter la direccion del id a la pila de EXP y eltipoa la de tipos
	var = p[-2]
	esteScope = TablaVariables[scope[len(scope)-1]]
	if var in esteScope:
		if esteScope[var]['dim'] < 1:
			dirV = esteScope[var]['dirVirtual']
			PExps.push(dirV)
			PTipos.push(esteScope[var]['tipo'])
		else:
			PExps.push(var)
			PTipos.push(esteScope[var]['tipo'])
	else:
		if TablaVariables['global'][var]['dim'] < 1:
			dirV = TablaVariables['global'][var]['dirVirtual']
			PExps.push(dirV)
			PTipos.push(TablaVariables['global'][var]['tipo'])
		else:
			PExps.push(var)
			PTipos.push(TablaVariables['global'][var]['tipo'])

#Recibe: PExps.pop() como right_operand, left_operand y 
#        PTipos.pop() como right_type, left_type
#Regresa: No aplica
#Cuadruplos: =
#Donde se usa: asignacion
#Que hace: crea cuadruplo de asignacion con su respectiva validacion
def p_checaasigna(p):
	'''checaasigna :'''
	#checar los tipos del '=' 
	right_operand = PExps.pop()
	right_type = PTipos.pop()
	left_operand = PExps.pop()
	left_type = PTipos.pop()
	operator = '='
	result_type = getTipo(left_type, right_type, operator)
	if result_type is not 'ERROR':
		quadAux = [operator, right_operand, 0, left_operand]
		quads.append(quadAux)
	else:
		print "Linea {0}: type mismatched".format(lexer.lineno)
		sys.exit()

#Recibe: PTipos.pop() como exp_type
#Regresa: No aplica
#Cuadruplos: GoToF
#Donde se usa: condicion, ciclo
#Que hace: valida que las expresiones sean booleanas
def p_checaExp(p):
	'''checaExp :'''
	#todas las exp de condiciones deben ser boleanas
	exp_type = PTipos.pop()
	if(exp_type != 'boleano'):
		print "Linea {0}: type mismatched".format(lexer.lineno)
		sys.exit()
	else:
		result = PExps.pop()
		quadAux = ['GotoF', result,0,0]
		quads.append(quadAux)
		PSaltos.push(len(quads)-1)

#Recibe: PSaltos.pop() como end
#Regresa: No aplica
#Cuadruplos: No aplica
#Donde se usa: s6
#Que hace: completa el cuadruplo del if
def p_finIFELSE(p):
	'''finIFELSE :'''
	#Final del if else y rellenar el cuadruplo
	end = PSaltos.pop()
	quadAux = quads[end]
	quadAux[3] = len(quads)	
	quads[end] = quadAux

#Recibe: PSaltos.pop() como false
#Regresa: No aplica
#Cuadruplos: 'Goto'
#Donde se usa: s6
#Que hace: crea cuadruplo de else, y completa el del if
def p_entroElse(p):
	'''entroElse :'''
	#entro al else y rellena cuadruplo de if
	false = PSaltos.pop()
	quadAux = ['Goto', 0,0,0]
	quads.append(quadAux)
	quadAux = quads[false]
	quadAux[3] = len(quads)	
	quads[false] = quadAux
	PSaltos.push(len(quads)-1)

#Recibe: PSalitos.pop() como end
#Regresa: No aplica
#Cuadruplos: No aplica
#Donde se usa: s6
#Que hace: completa el cuadruplo del if
def p_finIF(p):
	'''finIF :'''
	#final del if rellena cuadruplo
	end = PSaltos.pop()
	quadAux = quads[end]
	quadAux[3] = len(quads)	
	quads[end] = quadAux

#Recibe: No aplica
#Regresa: No aplica
#Cuadruplos: No aplica
#Donde se usa: ciclo
#Que hace: inserta direccion a la pila de saltos
def p_subirWhile(p):
	'''subirWhile :'''
	#saber a donde regresarme en el while(antes de la expresion)
	PSaltos.push(len(quads))

#Recibe: PSaltos.pop() como end
#Regresa: No aplica
#Cuadruplos: 'Goto'
#Donde se usa: ciclo
#Que hace: crea cuadruplo del regreso del while y 
#          completa el cuadruplo despues de la validacion
def p_subeWhile(p):
	'''subeWhile :'''
	#regresarme a la expresion del while
	end = PSaltos.pop()
	regreso = PSaltos.pop()
	quadAux = ['Goto', 0, 0,regreso]
	quads.append(quadAux)
	#llenar con cont el quads[end]
	quadAux = quads[end]
	quadAux[3] = len(quads)
	quads[end] = quadAux

#Recibe: p[-1]
#Regresa: No aplica
#Cuadruplo: cuadruplo 'meter', 'print'
#Donde se usa: escribirS
#Que hace: crea el quad para meter el string a memoria y luego desplegarlo
def p_mostrar_expresion(p):
	'''mostrar_expresion : '''
	#ya no muestra, ahora es para crear el cuadruplo de print
	global contCons
	contCons = contCons + 1
	if contCons > contCons:
		print "Linea {0}: Se acabo la memoria".format(lexer.lineno)
		sys.exit()
	global funcCons
	funcCons = funcCons + 1
	quadAux = ['meter', p[-1], 0, contCons-1]
	quads.append(quadAux)
	quadAux = ['print',0 ,0,contCons-1]
	quads.append(quadAux)
	expresion = ""

#Recibe: No aplica 
#Regresa: No aplica
#Cuadruplo: No aplica
#Donde se usa: llamarVoid, llamarFuncion
#Que hace: checa que no falten parametros al acabar de leer los argumentos
def p_checaResto(p):
	'''checaResto :'''
	#checa que el length de los parametros y argumentos sea el mismo
	global k
	global parametros
	if not(k == 1 and len(parametros)==0):
		if (k != len(parametros)):
			print "Linea {0}: Mal numero de parametros".format(lexer.lineno)
			sys.exit()

#Recibe: p[-6] como pocedure
#Regresa: No aplica
#Cuadruplo: cuadruplo 'ERA', 'GOSUB'
#Donde se usa: llamarVoid, llamarFuncion
#Que hace: crea el quad del tamaño de la funcion
#y del cuadruplo al que tiene que dirigirse
def p_GOSUB(p):
	'''GOSUB :'''
	#para hacer los quads de las funciones
	procedure = p[-6]
	size = directorioFunciones[procedure]['size']
	quadDestino = directorioFunciones[procedure]['quad']
	quadAux = ['ERA',procedure, size,0]#quad con el size de la funcion
	quads.append(quadAux)
	PEra.push(len(quads)+1)
	quadAux = ['GOSUB',procedure ,quadDestino,0]#cuad para saber a donde subir
	quads.append(quadAux)

#Recibe: No aplica
#Regresa: No aplica
#Cuadruplo: Ninguno
#Donde se usa: llamarFuncion, llamarVoid
#Que hace: checa que una funcion haya sido declarada
def p_checaFuncion(p):
	'''checaFuncion :'''
	#tomar los parametros de una funcion
	procedure = p[-1]
	global parametros
	global k 
	k = 1
	if procedure not in scope:
		print "Linea {0}: Funcion no declarada".format(lexer.lineno)
		sys.exit()
	else:
		parametros = directorioFunciones[procedure]['param']
		global direcciones
		direcciones = directorioFunciones[procedure]['direcciones']

#Recibe: PExps.pop() como argumento, PTipos.pop() como tipoArg
#Regresa: No aplica
#Cuadruplo: cuadruplo 'PARAMETER'
#Donde se usa: args
#Que hace: checa que el argumento y el parametro de la funcion
#sean del mismo tipo
def p_checaArg(p):
	'''checaArg :'''
	#checa el argumento x con el parametro x
	global k
	global parametros
	global direcciones
	argumento = PExps.pop()
	tipoArg = PTipos.pop()
	if tipoArg != parametros[k-1]:
		print "Linea {0}: Type mismatched in function".format(lexer.lineno)
		sys.exit()
	else:
		quadAux = ["PARAMETER", argumento, direcciones[k-1], 0]
		quads.append(quadAux)

def p_masArgs(p):
	'''masArgs :'''
	#si hay mas argumentos k = k+1
	global k
	k = k+1
#Recibe: PExps.pop() como right_operand, left_operand
#PTipos.pop() como right_type, left_type
#POper.pop() como operator
#Regresa: No aplica
#Cuadruplo: cuadruplo '&&', '||'
#Donde se usa: s11
#Que hace: crea el cuadruplo para calcular AND y OR
#de dos expresiones cuyos tipos sean compatibles
def p_resolvANDOR(p):
	'''resolvANDOR :'''
	#checa tipos de && y ||
	if POper.size() is not 0:
		if POper.top() == "&&" or POper.top() == "||":
			right_operand = PExps.pop()
			right_type = PTipos.pop()
			left_operand = PExps.pop()
			left_type = PTipos.pop()
			operator = POper.pop()
			result_type = getTipo(left_type, right_type, operator)
			if result_type is not 'ERROR':
				global contTemps
				result = contTemps
				contTemps = contTemps + 1
				if contTemps > limiteTemps:
					print "Linea {0}: Se acabo la memoria".format(lexer.lineno)
					sys.exit()
				global funcTemp
				funcTemp = funcTemp + 1
				quadAux = [operator, left_operand, right_operand, result]
				quads.append(quadAux)
				PExps.push(result)
				PTipos.push(result_type)
			else:
				print "Linea {0}: Type Mismatched".format(lexer.lineno)
				sys.exit()

#Recibe: PExps.pop() como right_operand, left_operand
#PTipos.pop() como right_type, left_type
#POper.pop() como operator
#Regresa: No aplica
#Cuadruplo: cuadruplo '<','>','<=','>=','==','!='
#Donde se usa: s12,
#Que hace: crea el cuadruplo para checar logica
#de dos expresiones cuyos tipos sean compatibles
def p_resolvRel(p):
	'''resolvRel :'''
	#checa los tipos de <, >, <> etc
	if POper.size() is not 0:
		if POper.top() == "<" or  POper.top() == ">" or POper.top() == "==" or POper.top() == "<=" or POper.top() == "!=" or POper.top() == ">=":
			right_operand = PExps.pop()
			right_type = PTipos.pop()
			left_operand = PExps.pop()
			left_type = PTipos.pop()
			operator = POper.pop()
			result_type = getTipo(left_type, right_type, operator)
			if result_type is not 'ERROR':
				global contTemps
				result = contTemps
				contTemps = contTemps + 1
				if contTemps > limiteTemps:
					print "Linea {0}: Se acabo la memoria".format(lexer.lineno)
					sys.exit()
				global funcTemp
				funcTemp = funcTemp + 1
				quadAux = [operator, left_operand, right_operand, result]
				quads.append(quadAux)
				PExps.push(result)
				PTipos.push(result_type)
			else:
				print "Linea {0}: Type Mismatched".format(lexer.lineno)
				sys.exit()

#Recibe: PExps.pop() como right_operand, left_operand
#PTipos.pop() como right_type, left_type
#POper.pop() como operator
#Regresa: No aplica
#Cuadruplo: cuadruplo '+'.'-'
#Donde se usa: exp
#Que hace: crea el cuadruplo para sumar o restar
#de dos expreiones cuyos tipos sean compatibles
def p_resolvBasic(p):
	'''resolvBasic :'''
	#checa los tipos de la suma y resta
	if POper.size() is not 0:
		if POper.top() is '+' or POper.top() is '-':
			right_operand = PExps.pop()
			right_type = PTipos.pop()
			left_operand = PExps.pop()
			left_type = PTipos.pop()
			
			operator = POper.pop()
			result_type = getTipo(left_type, right_type, operator)
			if result_type is not 'ERROR':
				global contTemps
				result = contTemps
				contTemps = contTemps + 1
				if contTemps > limiteTemps:
					print "Linea {0}: Se acabo la memoria".format(lexer.lineno)
					sys.exit()
				global funcTemp
				funcTemp = funcTemp + 1
				quadAux = [operator, left_operand, right_operand, result]
				quads.append(quadAux)
				PExps.push(result)
				PTipos.push(result_type)
			else:
				print "Linea {0}: Type Mismatched".format(lexer.lineno)
				sys.exit()

#Recibe: PExps.pop() como right_operand, left_operand
#PTipos.pop() como right_type, left_type
#POper.pop() como operator
#Regresa: No aplica
#Cuadruplo: cuadruplo '*', '/', '%'
#Donde se usa: termino
#Que hace: crea el cuadruplo para multiplicar, dividir o sacar mod
#de dos expresiones cuyos tipos sean compatibles
def p_resolvComp(p):
	'''resolvComp :'''
	#checa los tipos de * / y %
	if POper.size()is not 0:
		if POper.top() is '*' or POper.top() is '/' or POper.top() is '%':
			right_operand = PExps.pop()
			right_type = PTipos.pop()
			left_operand = PExps.pop()
			left_type = PTipos.pop()
			operator = POper.pop()
			result_type = getTipo(left_type, right_type, operator)
			if result_type is not 'ERROR':
				global contTemps
				result = contTemps
				contTemps = contTemps + 1
				if contTemps > limiteTemps:
					print "Linea {0}: Se acabo la memoria".format(lexer.lineno)
					sys.exit()
				global funcTemp
				funcTemp = funcTemp +1
				quadAux = [operator, left_operand, right_operand, result]
				quads.append(quadAux)
				PExps.push(result)
				PTipos.push(result_type)
			else:
				print "Linea {0}: Type Mismatched".format(lexer.lineno)
				sys.exit()

#Recibe: p[-1] como oper
#Regresa: No aplica
#Cuadruplo: Ninguno
#Donde se usa: asignacion, s10, s12, s13, s15, factor
#Que hace: inserta el operador en la pila de operadores
def p_operPila(p):
	'''operPila :'''
	#meter el operador a la pila de operadores
	oper = p[-1]
	POper.push(oper)

#Recibe: No aplica
#Regresa: No aplica
#Cuadruplo: Ninguno
#Donde se usa: factor
#Que hace: Saca el fondo falso de la pila de expresiones
def p_sacaPila(p):
	'''sacaPila :'''
	#sacar el operador de la pila
	POper.pop()

#Recibe: p[-2] como var
#Regresa: No aplica
#Cuadruplo: No aplica
#Donde se usa: s17
#Que hace: inserta la dirección de la variable a la pila de expresiones
#insertar el tipo de la variable a la pila de tipos
def p_varPila(p):
	'''varPila :'''
	#meter la direccion de una variable a la pila de exp y su tipo
	var = p[-2]
	esteScope = TablaVariables[scope[len(scope)-1]]
	if var in esteScope:
		if esteScope[var]['dim'] < 1:
			dirV = esteScope[var]['dirVirtual']
			PExps.push(dirV)
			PTipos.push(esteScope[var]['tipo'])
		else:
			PExps.push(var)
			PTipos.push(esteScope[var]['tipo'])
	else:
		if TablaVariables['global'][var]['dim'] < 1:
			dirV = TablaVariables['global'][var]['dirVirtual']
			PExps.push(dirV)
			PTipos.push(TablaVariables['global'][var]['tipo'])
		else:
			PExps.push(var)
			PTipos.push(TablaVariables['global'][var]['tipo'])

#Recibe: p[-7] como funcion
#Regresa: No aplica
#Cuadruplo: Ninguno
#Donde se usa: llamarFuncion
#Que hace: inserta a la pila de expresiones su dirección virtual de retorno
#insertr su tipon a la pila de tipos
def p_funcionPila(p):
	'''funcionPila :'''
	#meter la fucnion a la pila de exp y su tipo
	funcion = p[-7]
	regresa = 	directorioFunciones[funcion]['regresa']
	PExps.push(regresa)
	PTipos.push(directorioFunciones[funcion]['tipo'])

#Recibe: No aplica
#Regresa: No aplica
#Cuadruplo: cuadruplo 'meter'
#Donde se usa: factor
#Que hace: inserta a la pila de expresiones una variable entera
#crea elcuadruplo para meterla a la memoria
def p_enteroPila(p):
	'''enteroPila :'''
	#meter enteros a la pila de exp y su tipo
	global contCons
	PExps.push(contCons)
	contCons = contCons + 1
	if contCons > contCons:
		print "Linea {0}: Se acabo la memoria".format(lexer.lineno)
		sys.exit()
	global funcCons
	funcCons = funcCons + 1
	quadAux = ['meter', p[-1], 0, contCons-1]
	quads.append(quadAux)
	PTipos.push('entero')	

#Recibe: No aplica
#Regresa: No aplica
#Cuadruplo: cuadruplo 'meter'
#Donde se usa: factor
#Que hace: inserta a la pila de expresiones una variable doble
#crea elcuadruplo para meterla a la memoria
def p_doblePila(p):
	'''doblePila :'''
	#meter dobles a pila de exp y su tipo
	global contCons
	PExps.push(contCons)
	contCons = contCons + 1
	if contCons > contCons:
		print "Linea {0}: Se acabo la memoria".format(lexer.lineno)
		sys.exit()
	global funcCons
	funcCons = funcCons + 1
	quadAux = ['meter', p[-1], 0, contCons-1]
	quads.append(quadAux)
	PTipos.push('doble')

#Recibe: No aplica
#Regresa: No aplica
#Cuadruplo: cuadruplo 'meter'
#Donde se usa: factor
#Que hace: inserta a la pila de expresiones una variable boleana
#crea elcuadruplo para meterla a la memoria
def p_boolPila(p):
	'''boolPila :'''
	#meter boleanos a pila de exp y su tipo
	global contCons
	PExps.push(contCons)
	contCons = contCons + 1
	if contCons > contCons:
		print "Linea {0}: Se acabo la memoria".format(lexer.lineno)
		sys.exit()
	global funcCons
	funcCons = funcCons + 1
	quadAux = ['meter', p[-1], 0, contCons-1]
	quads.append(quadAux)
	PTipos.push('boleano')	

#Recibe: No aplica
#Regresa: No aplica
#Cuadruplo: Ninguno
#Donde se usa: crearArco
#Que hace: define el proximo tipo de variable de figura
def p_nuevo_objeto_arco(p):
	'''nuevo_objeto_arco :'''
	#proximo objeto a crear
	ultimoTipo.append('arco')

#Recibe: No aplica
#Regresa: No aplica
#Cuadruplo: Ninguno
#Donde se usa: crearCirculo
#Que hace: define el proximo tipo de variable de figura
def p_nuevo_objeto_circulo(p):
	'''nuevo_objeto_circulo :'''
	#proximo objeto a crear
	ultimoTipo.append('circulo')

#Recibe: No aplica
#Regresa: No aplica
#Cuadruplo: Ninguno
#Donde se usa: crearCuadro
#Que hace: define el proximo tipo de variable de figura
def p_nuevo_objeto_cuadro(p):
	'''nuevo_objeto_cuadro :'''
	#proximo objeto a crear
	ultimoTipo.append('cuadro')

#Recibe: No aplica
#Regresa: No aplica
#Cuadruplo: Ninguno
#Donde se usa: crearTriangulo
#Que hace: define el proximo tipo de variable de figura
def p_nuevo_objeto_trian(p):
	'''nuevo_objeto_trian :'''
	#proximo objeto a crear
	ultimoTipo.append('triangulo')

#Recibe: No aplica
#Regresa: No aplica
#Cuadruplo: Ninguno
#Donde se usa: crearLinea
#Que hace: define el proximo tipo de variable de figura
def p_nuevo_objeto_linea(p):
	'''nuevo_objeto_linea :'''
	#proximo objeto a crear
	ultimoTipo.append('linea')

#Recibe: PExps.pop() como y2pos, y1pos, x1pos, x2pos
#PTipos.pop() como tipoUno, tipoDos, tipoTres, tipoCuatro
#Regresa: No aplica
#Cuadruplo: cuadruplo 'l'
#Donde se usa: crearLinea
#Que hace: crea el cuadruplo con las coordenadas para la linea
def p_quadLinea(p):
	'''quadLinea :'''
	#crear el quad de linea
	y2pos = PExps.pop()
	x2pos = PExps.pop()
	y1pos = PExps.pop()
	x1pos = PExps.pop()
	tipoUno = PTipos.pop()
	tipoDos = PTipos.pop()
	tipoTres = PTipos.pop()
	tipoCuatro = PTipos.pop()
	if (tipoUno != "boleano") and( tipoDos != "boleano") and (tipoTres != "boleano") and( tipoCuatro != "boleano"):
		lista = [x1pos, y1pos, x2pos, y2pos]
		quadAux = ['l', lista, 0, 0]
		quads.append(quadAux)
	else:
		print "Linea {0}: Error al crear figura. Type Mismatched".format(lexer.lineno)
		sys.exit()

#Recibe: P[-2] como una funcion
#Regresa: No aplica
#Cuadruplo: cuadruplo 'a', 'r', 't' o 'c'
#Donde se usa: crearCuadro, crearArco, crearTriangulo, crearLinea
#Que hace: Define la proxima figura a creear
def p_quadFigura(p):
	'''quadFigura :'''
	#saber que figura estoy por crear
	if p[-2] == "crearArco":
		quadAux = ['a', 0, 0, 0]
		quads.append(quadAux)
	else:
		if p[-2] == "crearCuadro":
			quadAux = ['r', 0, 0, 0]
			quads.append(quadAux)
		else:
			if p[-2] == "crearTriangulo":
				quadAux = ['t', 0, 0, 0]
				quads.append(quadAux)
			else:
				if p[-2] == "crearCirculo":
					quadAux = ['c', 0, 0, 0]
					quads.append(quadAux)

#Recibe: p[-12] como nombre, PExps.pop() como alto, ancho, ypos, xpos
#p[-2] como color, PTipos.pop() como tipoUno, tipoDos, tipoTres, tipoCuatro
#Regresa: No aplica
#Cuadruplo: cuadruplo 'k'
#Donde se usa: baseFigura
#Que hace: crea las coordenadas para las figuras
def p_restoCrear(p):
	'''restoCrear :'''
	#sacar los parametros para crear
	nombre = p[-12]
	ancho = PExps.pop()
	alto = PExps.pop()
	ypos = PExps.pop()
	xpos = PExps.pop()
	color = p[-2]
	tipoUno = PTipos.pop()
	tipoDos = PTipos.pop()
	tipoTres = PTipos.pop()
	tipoCuatro = PTipos.pop()
	if (tipoUno != "boleano") and( tipoDos != "boleano") and (tipoTres != "boleano") and( tipoCuatro != "boleano"):
		lista = [ancho, alto, xpos, ypos]
		quadAux = ['k', nombre, lista, color]
		quads.append(quadAux)
	else:
		print "Linea {0}: Error al crear figura. Type Mismatched".format(lexer.lineno)
		sys.exit()

#Recibe: p[-17] como nombre, PExps.pop() como x1,x2,x3,y1,y2,y3
#p[-2] como color, PTipos.pop() como tipoUno, tipoDos, tipoTres, tipoCuatro, tipoCinco, tipoSeis
#Regresa: No aplica
#Cuadruplo: cuadruplo 'k'
#Donde se usa: baseFiguraTriangulo
#Que hace: crea las coordenadas para el triangulo
def p_restoCrearTriangulo(p):
	'''restoCrearTriangulo :'''
	#sacar los parametros para crear
	nombre = p[-17]
	y3 = PExps.pop()
	x3 = PExps.pop()
	y2 = PExps.pop()
	x2 = PExps.pop()
	y1 = PExps.pop()
	x1 = PExps.pop()
	color = p[-2]
	tipoUno = PTipos.pop()
	tipoDos = PTipos.pop()
	tipoTres = PTipos.pop()
	tipoCuatro = PTipos.pop()
	tipoCinco = PTipos.pop()
	tipoSeis = PTipos.pop()
	if (tipoUno != "boleano") and( tipoDos != "boleano") and (tipoTres != "boleano") and( tipoCuatro != "boleano") and( tipoCinco != "boleano") and( tipoSeis != "boleano"):
		lista = [x1,y1,x2,y2,x3,y3]
		quadAux = ['k', nombre, lista, color]
		quads.append(quadAux)
	else:
		print "Linea {0}: Error al crear figura. Type Mismatched".format(lexer.lineno)
		sys.exit()

#Recibe: PExps.pop() como var, PTipos.pop() como tipo
#Regresa: No aplica
#Cuadruplo: cuaddruplo 'verifica', '.'
#Donde se usa: s20
#Que hace: Mueve una variable de la pila de expresiones a la de arreglos
def p_usaArr(p):
	'''usaArr :'''
	#se usa una variable dimensionada
	var = PExps.pop()
	tipo = PTipos.pop()
	PArreglos.push(var)
	PTArreglos.push(tipo)

#Recibe: PTipos.pop() como un tipo
#Regresa: No aplica
#Cuadruplo: cuaddruplo 'verifica', '.'
#Donde se usa: p_20
#Que hace: Verificar que el indice este en el rango
#Suma la dirección virtual base al indice
def p_usaArr1(p):
	'''usaArr1 :'''
	#se termina gramatica de variable dimensionada
	tipo = PTipos.pop()
	if tipo == 'entero':
		dim = PExps.pop()
		var = PArreglos.pop()
		esteScope = TablaVariables[scope[len(scope)-1]]
		if var in esteScope:
			limite = esteScope[var]['dim']
			dirV = esteScope[var]['dirVirtual']
			tipo = PTArreglos.pop()
		else:
			limite= TablaVariables['global'][var]['dim']
			dirV = TablaVariables['global'][var]['dirVirtual']
			tipo = PTArreglos.pop()
		quadAux = ['verif',0,dim,limite-1]
		quads.append(quadAux)
		global contDirs
		result = contDirs
		contDirs = contDirs + 1
		if contDirs > contDirs:
			print "Linea {0}: Se acabo la memoria".format(lexer.lineno)
			sys.exit()
		global funcDirs
		funcDirs = funcDirs + 1		
		quadAux = ['.', dim, dirV,result]
		quads.append(quadAux)
		PExps.push(result)
		PTipos.push(tipo)
	else:
		print "Linea {0}: Indice no entero".format(lexer.lineno)
		sys.exit()

#Recibe: p[-1] como una variable
#Regresa: no aplica
#Cuadruplos: ninguno
#Donde se usa: asignacion, pedirValor, s17, 
#Que hace: Checa que la variable haya sido declarada
def p_checa_existe(p):
	'''checa_existe :'''
	#checar si una variable existe
	var = p[-1]
	if var not in TablaVariables["global"] and var not in TablaVariables[scope[len(scope)-1]]:
		print "Linea {0}: Variable inexistente".format(lexer.lineno)
		sys.exit()

# Manejar errores
def p_error(p):
	print "Linea {1}: Mala sintaxis en la entrada en '{0}'".format(p.value, lexer.lineno)
	sys.exit()

# Construir el parser
parser = yacc.yacc()

# Main
if __name__ == '__main__':
	if (len(sys.argv) > 1):
		file = sys.argv[1]
		# Abrir archivo, almacenar informacion y cerrarlo
		try:
			f = open(file,'r')
			data = f.read()
			f.close()
			if (parser.parse(data, tracking=True) == 'PROGRAM COMPILED'): 
				print '----------------------------------------------'
				print "PARTUM FIGURIS BY: PEDRO ESPARZA & JAVIER CRUZ"
				print '----------------------------------------------'
				maquina.ejecuta(quads, memoria)
				print '----------------------------------------------'
		except EOFError:
			print(EOFError)
	else:
		print('File missing')
