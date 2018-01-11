
cuboSemantico = {
		"entero" : {
			"entero" : {
				"+" : "entero",
				"-" : "entero",
				"*" : "entero",
				"/" : "entero",
				"%" : "entero",
				"=" : "entero",
				"==" : "boleano",
				"!=" : "boleano",
				">" : "boleano",
				"<" : "boleano",
				">=" : "boleano",
				"<=" : "boleano",
				"&&" : "ERROR",
				"||" : "ERROR"
			},
			"doble" : {
				"+" : "doble",
				"-" : "doble",
				"*" : "doble",
				"/" : "doble",
				"%" : "doble",
				"=" : "ERROR",
				"==" : "boleano",
				"!=" : "boleano",
				">" : "boleano",
				"<" : "boleano",
				">=" : "boleano",
				"<=" : "boleano",
				"&&" : "ERROR",
				"||" : "ERROR"
			},
			"boleano" : {
				"+" : "ERROR",
				"-" : "ERROR",
				"*" : "ERROR",
				"/" : "ERROR",
				"%" : "ERROR",
				"=" : "ERROR",
				"==" : "ERROR",
				"!=" : "ERROR",
				">" : "ERROR",
				"<" : "ERROR",
				">=" : "ERROR",
				"<=" : "ERROR",
				"&&" : "ERROR",
				"||" : "ERROR"
			}
		},
		"doble" : {
			"entero" : {
				"+" : "doble",
				"-" : "doble",
				"*" : "doble",
				"/" : "doble",
				"%" : "doble",
				"=" : "ERROR",
				"==" : "boleano",
				"!=" : "boleano",
				">" : "boleano",
				"<" : "boleano",
				">=" : "boleano",
				"<=" : "boleano",
				"&&" : "ERROR",
				"||" : "ERROR"
			},
			"doble" : {
				"+" : "doble",
				"-" : "doble",
				"*" : "doble",
				"/" : "doble",
				"%" : "doble",
				"=" : "doble",
				"==" : "boleano",
				"!=" : "boleano",
				">" : "boleano",
				"<" : "boleano",
				">=" : "boleano",
				"<=" : "boleano",
				"&&" : "ERROR",
				"||" : "ERROR"
			},
			"boleano" : {
				"+" : "ERROR",
				"-" : "ERROR",
				"*" : "ERROR",
				"/" : "ERROR",
				"%" : "ERROR",
				"=" : "ERROR",
				"==" : "ERROR",
				"!=" : "ERROR",
				">" : "ERROR",
				"<" : "ERROR",
				">=" : "ERROR",
				"<=" : "ERROR",
				"&&" : "ERROR",
				"||" : "ERROR"
			}
		},
		"boleano" : {
			"entero" : {
				"+" : "ERROR",
				"-" : "ERROR",
				"*" : "ERROR",
				"/" : "ERROR",
				"%" : "ERROR",
				"=" : "ERROR",
				"==" : "ERROR",
				"!=" : "ERROR",
				">" : "ERROR",
				"<" : "ERROR",
				">=" : "ERROR",
				"<=" : "ERROR",
				"&&" : "ERROR",
				"||" : "ERROR"
			},
			"doble" : {
				"+" : "ERROR",
				"-" : "ERROR",
				"*" : "ERROR",
				"/" : "ERROR",
				"%" : "ERROR",
				"=" : "ERROR",
				"==" : "ERROR",
				"!=" : "ERROR",
				">" : "ERROR",
				"<" : "ERROR",
				">=" : "ERROR",
				"<=" : "ERROR",
				"&&" : "ERROR",
				"||" : "ERROR"
			},
			"boleano" : {
				"+" : "ERROR",
				"-" : "ERROR",
				"*" : "ERROR",
				"/" : "ERROR",
				"%" : "ERROR",
				"=" : "boleano",
				"==" : "boleano",
				"!=" : "boleano",
				">" : "ERROR",
				"<" : "ERROR",
				">=" : "ERROR",
				"<=" : "ERROR",
				"&&" : "boleano",
				"||" : "boleano"
			}
		}
	}
	

def getTipo(op1, op2, oper):
	return cuboSemantico[op1][op2][oper]
	