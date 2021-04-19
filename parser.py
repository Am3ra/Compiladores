import ply.yacc as yacc
import pickle
from lexer import lexer
from lexer import tokens
from enum import Enum
# from semanticAnalyzer import SemanticAnalyzer

#! TIPOS DISPONIBLES EN EL LENGUAJE:
# 1) TIPOS SIMPLES
# 2) LOS KEYS DE LA TABLA DE CLASES 

# simple_types + symbol_table_classes.keys()


#! Juntar simbolos?


class SemanticAnalyzer():
	def __init__(self, input):
		self.input = input
		self.main: MainNode = parser.parse(input)
		self.symbol_table_list = [{}]


	def analisis_semantico(self,filename):
		#Falta hacer el analysis
		self.main.analyze(self)
		
		f = open(filename,'wb')
		pickle.dump(self.main,f) # Se serializa el AST
		f.close()

	def declarar_class(self, dec):
		self.check_if_declared_global(dec, "CLASS")
		self.symbol_table_classes[dec["id"]] = dec

	
	def declare_symbol_class(self, dec, class_name, type):
		# self.check_if_declared_class(self,dec,class_name)
		self.check_if_symbol_declared_scope(dec,self.symbol_table_classes[class_name])
		self.symbol_table_classes[class_name][type][dec["id"]] = dec

def declarar_symbol_scopes(dec,scopes):
	if (check_if_symbol_declared_scopes(dec["id"],scopes)):
		raise SemanticError("{0} already declared".format(dec["id"]))
	scopes[-1][dec["id"]] = dec

def check_if_symbol_declared_scopes(id,scopes):
	for scope in scopes:
		if (scope.get(id) is not None):
			return scope.get(id)
	return False
	

# SemanticAnalyzer(text).analisis_semantico()

class Node():
	def analyze(self, analyzer: SemanticAnalyzer):
		'''Complete Semantic analysis of this node '''
		pass


class MainNode(Node):
	def __init__(self, declaraciones, main):
		self.declaraciones = declaraciones
		self.main = main

	def analyze(self, analyzer: SemanticAnalyzer):
		for dec  in self.declaraciones:
			dec.analyze(analyzer)

		for estatuto in self.main:
			estatuto.analyze(analyzer)

	def __str__(self):
		return "{0}".format(("Programa", self.declaraciones, self.main))


class VarDecNode(Node):
	def __init__(self, dec):
		self.dec = dec

	def __str__(self):
		return "{0}".format(("VARDEC", self.dec))

	def __repr__(self):
		return "{0}".format(("VARDEC", self.dec))

	def analyze(self, analyzer: SemanticAnalyzer):
		# print("Symbol list:",analyzer.symbol_table_list)
		declarar_symbol_scopes(self.dec,analyzer.symbol_table_list)


class FuncDecNode(Node):
	def __init__(self, dec):
		self.dec = dec
		#{"name": p[2], "params": p[4], "return_op": p[6],
		# ""estatutos": p[7]}

	def __str__(self):
		return "{0}".format(("FUNCDEC", self.dec))

	def __repr__(self):
		return "{0}".format(("FUNCDEC", self.dec))

	def analyze(self, analyzer: SemanticAnalyzer):
		## CHECAR ID GLOBAL
		if (check_if_symbol_declared_scopes(self.dec["id"], analyzer.symbol_table_list) ):
			raise SemanticError("Symbol declared with same name.")


		# print(analyzer.symbol_table_list)

		## CREAR DIC VACIO
		analyzer.symbol_table_list[0][self.dec["id"]] = temp_symbol_table = {

			"id": self.dec["id"],
			"parameters": self.dec["params"],
			"return_type":self.dec["return_op"]
		}
		

		analyzer.symbol_table_list.append({})
		# print("push to list")
		# print(analyzer.symbol_table_list)

		#Declarar todos los params

		## DECLARAR PARAMETROS
		for param in self.dec["params"]:
			declarar_symbol_scopes(param,analyzer.symbol_table_list)
		for estatuto in self.dec["body"]:
			estatuto.analyze(analyzer)
		## Analyzar CUERPO
		# if has return type
		if self.dec["return_op"]:
			for estatuto in self.dec["body"]:
				if estatuto is ReturnNode: # PseudoCode
					if estatuto.type != self.dec["return_op"]:
						SemanticError("Return of Wrong Type!")
			else:
				SemanticError("Function is Missing Return!")
		
		# print(analyzer.symbol_table_list)

		analyzer.symbol_table_list.pop()

		# print(analyzer.symbol_table_list)

class SemanticError(Exception):
	pass

class ClassDecNode(Node):
	def __init__(self, dec):
		self.dec = dec
		'''('CLASSDEC', {'id': 'team', 'inheritance': None, 
		'body': {'attributes': [], 'methods': 
			[{'id': 'team', 'params': [], 'return_op': None, 
			'body': {'Estatutos': []}}]}})'''

	def __str__(self):
		return "{0}".format(("CLASSDEC", self.dec))

	def __repr__(self):
		return "{0}".format(("CLASSDEC", self.dec))

	def analyze(self, analyzer: SemanticAnalyzer):
		# Checar que si existe la herencia

		
		# Checar el id
		check_if_symbol_declared_scopes(self.dec["id"],analyzer.symbol_table_list)
		# Checar nombres de funcs y vars
		analyzer.symbol_table_list[0]["id"] = ({"id": self.dec["id"],"attributes":self.dec["attributes"],"methods":self.dec["methods"]})

		analyzer.symbol_table_list.append({})

		for attribute in self.dec["attributes"] :
			declarar_symbol_scopes(attribute, analyzer.symbol_table_list)

		for method in self.dec["methods"] :
			declarar_symbol_scopes(method, analyzer.symbol_table_list)

		## Agregar cosas inheritance
		# print(declarar_symbol_scopes)
		analyzer.symbol_table_list.pop()

		if (self.dec["inheritance"]):
			father = analyzer.symbol_table_list[0].get(self.dec["inheritance"])
			if (father is None):
				raise SemanticError("Inherits undeclared class")
			else:
				for attribute in father["attributes"]:
					analyzer.symbol_table_list[0][dec["id"]]["attributes"].setdefault(attribute,father[attribute])


# class BloqueNode(Node):
# 	def __init__(self, vars, estatutos):
# 		self.vars = vars
# 		self.estatutos = estatutos

# 	def __str__(self):
# 		return "{0}".format(("BLOQUE CODE", self.dec))

# 	def __repr__(self):
# 		return "{0}".format(("BLOQUE CODE", self.dec))

# 	def analyze(self, analyzer: SemanticAnalyzer):
# 		analyzer.symbol_table_vars_list+{} # Push new lexical scope


# 		for estatuto in self.estatutos:
# 			estatuto.analyze()

# 		analyzer.symbol_table_vars_list.pop() # pop lexical scope

class AssignNode(Node):
	def __init__(self, var, expresion):
		self.var = var
		self.expresion = expresion

	def __str__(self):
		return "{0}".format(("ASSIGN", self.dec))

	def __repr__(self):
		return "{0}".format(("ASSIGN", self.dec))

	def analyze(self, scope ,analyzer: SemanticAnalyzer):
		# Variable es metodo?
		if self.var["call_type"] == "method_call":
			SemanticError("Can't assign to a method")
		# Marcar como definido?
		variable = ""
		# Existe la variable?
		if self.var["call_type"] == "simple":
			pass
			# variable = variable_declarada_scopes(self.var["id"],scope)
		elif self.var["call_type"] == "attribute_call":
			#Check class table
			pass
		elif self.var["call_type"] == "Array":
			pass
		## Obtener tipo de variable?
		var_type = variable["type"]
		# La asignacion es de tipo correcto?
		## Analyzar expresion
		expr = self.expresion.analyze(scope)
		### Obtener tipo expresion

		if variable["tipo"] != expr["tipo"]:
			SemanticError("Asignacion de tipo incorrecto")

# FUNCIONA!

# ''' estatuto : asignacion
# 			| expresion
# 			| returns
# 			| llamada_funcion SEMICOLON
# 			| llamada_objeto SEMICOLON
# 			| var_def SEMICOLON
# 			| lectura
# 			| escritura
# 			| decision
# 			| repeticion '''

class BaseType(Enum):
	STRING = 1
	INT = 2
	FLOAT = 3
	BOOL = 4

# class ExpresionNode(Node):
# 	def __init__(self, type, children):
# 		self.dec = dec

# 	def __str__(self):
# 		return "{0}".format(("EXPR", self.dec))

# 	def __repr__(self):
# 		return "{0}".format(("EXPR", self.dec))

# 	def analyze(self, analyzer: SemanticAnalyzer):
		

#done
class UnopNode(Node):
	def __init__(self, operation, operand):
		self.operation = operation
		self.operand = operand

	def __str__(self):
		return "{0}".format(("UNOP", self.operation, self.operand))

	def __repr__(self):
		return "{0}".format(("UNOP", self.operation, self.operand))

	def analyze(self, analyzer: SemanticAnalyzer):
		operand_type = self.operand.analyze()

		if operand_type is not "int" or operand_type is not "float":
			SemanticError("Can only apply unary +/- to int or float")
		else:
			return operand_type

#done
class BinopNode(Node):
	def __init__(self, operation, lhs, rhs):
		self.operation = operation
		self.lhs = lhs
		self.rhs = rhs

	def __str__(self):
		return "{0}".format(("BINOP", self.operation, self.lhs,self.rhs))

	def __repr__(self):
		return "{0}".format(("BINOP", self.operation, self.lhs, self.rhs))

	def analyze(self, analyzer: SemanticAnalyzer):
		lh_type = self.lhs.analyze()
		rh_type = self.rhs.analyze()

		if lh_type != rh_type:
			SemanticError("Binary operations can only be done with same types")
		else:
			return lh_type

class CompareNode(BinopNode):
	def analyze(self, analyzer):
		lh_type = self.lhs.analyze()
		rh_type = self.rhs.analyze()

		if lh_type != rh_type:
			SemanticError("Binary operations can only be done with same types")
		else:
			return BaseType.BOOL


class PlusNode(BinopNode):
	def __str__(self):
		return "{0}".format(("PLUS", self.operation, self.lhs,self.rhs))

	def __repr__(self):
		return "{0}".format(("PLUS", self.operation, self.lhs, self.rhs))


class MinusNode(BinopNode):
	def __str__(self):
		return "{0}".format(("MINUS", self.operation, self.lhs,self.rhs))

	def __repr__(self):
		return "{0}".format(("MINUS", self.operation, self.lhs, self.rhs))

class TimesNode(BinopNode):
	def __str__(self):
		return "{0}".format(("TIMES", self.operation, self.lhs,self.rhs))

	def __repr__(self):
		return "{0}".format(("TIMES", self.operation, self.lhs, self.rhs))

class DivideNode(BinopNode):
	def __str__(self):
		return "{0}".format(("DIVIDE", self.operation, self.lhs,self.rhs))

	def __repr__(self):
		return "{0}".format(("DIVIDE", self.operation, self.lhs, self.rhs))

class EqualsNode(CompareNode):
	def __str__(self):
		return "{0}".format(("EQUALS", self.operation, self.lhs,self.rhs))

	def __repr__(self):
		return "{0}".format(("EQUALS", self.operation, self.lhs, self.rhs))

class NotEqualsNode(CompareNode):
	def __str__(self):
		return "{0}".format(("NOTEQ", self.operation, self.lhs,self.rhs))

	def __repr__(self):
		return "{0}".format(("NOTEQ", self.operation, self.lhs, self.rhs))

class GTNode(CompareNode):
	def __str__(self):
		return "{0}".format(("GTHAN", self.operation, self.lhs,self.rhs))

	def __repr__(self):
		return "{0}".format(("GTHAN", self.operation, self.lhs, self.rhs))

class LTNode(CompareNode):
	def __str__(self):
		return "{0}".format(("LTHAN", self.operation, self.lhs,self.rhs))

	def __repr__(self):
		return "{0}".format(("LTHAN", self.operation, self.lhs, self.rhs))

class ConstantNode(Node):
	def analyze(self, analyzer):
		return self.type_name

class BoolNode(ConstantNode):
	def __init__(self, value):
		self.value = value
		self.type_name = BaseType.BOOL

class FloatNode(ConstantNode):
	def __init__(self, value):
		self.value = value
		self.type_name = BaseType.FLOAT
		
class IntNode(ConstantNode):
	def __init__(self, value):
		self.value = value
		self.type_name = BaseType.INT

#!NOT DONE
class VarCallNode(Node):
	def __init__(self,id,call_type):
		self.id = id
		self.call_type = call_type
	
	def __str__(self):
		return "{0}".format(("VAR_CALL", self.operation, self.lhs,self.rhs))

	def __repr__(self):
		return "{0}".format(("VAR_CALL", self.operation, self.lhs, self.rhs))
		
	def analyze(self, analyzer):
		# Checar que existe
		var = check_if_symbol_declared_scopes(self.id,analyzer.symbol_table_list) 
		## CHECK CALL TYPE IS THE SAME AS VAR DIMS
		if var is not None:
			if var["defined"]:
				return var["type"]
			else:
				SemanticError("CAN'T CALL UNDEFINDED VAR {0}".format(self.id))
		else:
			SemanticError("CAN'T CALL UNDECLARED VAR {0}".format(self.id))


#DONE
class ReturnNode(Node):
	def __init__(self, expr):
		self.expr = expr

	def __str__(self):
		return "{0}".format(("RETURN", self.expr))

	def __repr__(self):
		return "{0}".format(("RETURN", self.epxr))

	def analyze(self, analyzer: SemanticAnalyzer):
		return self.expr.analyze()
		
class FuncCallNode(Node):
	def __init__(self, dec):
		self.dec = dec

	def __str__(self):
		return "{0}".format(("VARDEC", self.dec))

	def __repr__(self):
		return "{0}".format(("VARDEC", self.dec))

	def analyze(self, analyzer: SemanticAnalyzer):
		pass
		
class ObjectCallNode(Node):
	def __init__(self, dec):
		self.dec = dec

	def __str__(self):
		return "{0}".format(("VARDEC", self.dec))

	def __repr__(self):
		return "{0}".format(("VARDEC", self.dec))

	def analyze(self, analyzer: SemanticAnalyzer):
		pass

#!Siguiente entrega		
class ReadNode(Node):
	def __init__(self, dec):
		self.dec = dec

	def __str__(self):
		return "{0}".format(("VARDEC", self.dec))

	def __repr__(self):
		return "{0}".format(("VARDEC", self.dec))

	def analyze(self, analyzer: SemanticAnalyzer):
		# Checa que la variable exista, y sea de tipo string
		pass

#!Siguiente entrega		
class WriteNode(Node):
	def __init__(self, dec):
		self.dec = dec

	def __str__(self):
		return "{0}".format(("VARDEC", self.dec))

	def __repr__(self):
		return "{0}".format(("VARDEC", self.dec))

	def analyze(self, analyzer: SemanticAnalyzer):
		#checa que variable(s) exista(n)

		#analyzar arg punto
		
		declarar_symbol_scopes(self.dec,analyzer.symbol_table_list)

		
class ConditionNode(Node):
	def __init__(self, dec):
		self.dec = dec

	def __str__(self):
		return "{0}".format(("VARDEC", self.dec))

	def __repr__(self):
		return "{0}".format(("VARDEC", self.dec))

	def analyze(self, analyzer: SemanticAnalyzer):
		# print("Symbol list:",analyzer.symbol_table_list)
		# Checar que expresion condicion sea bool

		# Checar estatutos internos.
		declarar_symbol_scopes(self.dec,analyzer.symbol_table_list)

class LoopNode(Node):
	def __init__(self, dec):
		self.dec = dec

	def __str__(self):
		return "{0}".format(("VARDEC", self.dec))

	def __repr__(self):
		return "{0}".format(("VARDEC", self.dec))

	def analyze(self, analyzer: SemanticAnalyzer):
		# print("Symbol list:",analyzer.symbol_table_list)
		#Checar Condicion es bool

		#Checar estatutos internos
		declarar_symbol_scopes(self.dec,analyzer.symbol_table_list)


def p_programa(p):
	'''programa : declaraciones main '''
	p[0] = MainNode(p[1], p[2])


def p_declaraciones(p):
	'''declaraciones : empty '''
	p[0] = []


def p_declaraciones_variables(p):
	'''declaraciones : var_def SEMICOLON declaraciones '''
	p[0] = [VarDecNode(p[1])] + p[3]


def p_declaraciones_funciones(p):
	'''declaraciones : funcion_def declaraciones '''
	p[0] = [FuncDecNode(p[1])] + p[2]


def p_declaraciones_clases(p):
	'''declaraciones : clase_def declaraciones '''
	p[0] = [ClassDecNode(p[1])] + p[2]


def p_clase_def(p):
	'''clase_def : CLASS ID clase_op bloque_clase'''
	p[0] = ({"id" : p[2], "inheritance" : p[3], "attributes": p[4]["attributes"], "methods" : p[4]["methods"]})


def p_clase_op(p):
	''' clase_op : INHERIT ID 
				 | empty '''
	if(len(p) == 3):
		p[0] = p[2]
	else:
		p[0] = None


def p_bloque_clase(p):
	''' bloque_clase : LBRACE op_var op_func RBRACE'''
	p[0] = {"attributes":p[2], "methods" : p[3]}

'''
#! CAMBIO DE GRAMATICA 

op_func : funcion_def 

op_var : var_def op_var	

'''


def p_op_func(p):
	''' op_func : funcion_def op_func
				| empty'''
	if (len(p)==3):
		p[0] = [p[1]] + p[2]
	else:
		p[0] = []


def p_funcion_def(p):
	''' funcion_def : FUNC ID LPAREN params RPAREN return_option bloque_func'''
	p[0] = {"id": p[2], "params": p[4], "return_op": p[6],
			"body":p[7]}


def p_op_var(p):
	''' op_var : var_def SEMICOLON op_var
			   | empty'''
	if (len(p)==3):
		p[0] = [p[1]] + p[2]
	else:
		p[0] = []
		


def p_return_option(p):
	''' return_option : RET type_simple
					  | empty '''
	if(len(p) == 3):
		p[0] = p[2]
	else:
		p[0] = None

'''
#! PARAMS AHORA PUEDE SER EMPTY

#! CAMBIO EN GRAMATICA 
params_op : COMMA ID COLON type_simple params_op

'''

def p_params(p):
	''' params : var_def params_op
				| empty'''
	if(len(p) == 3):
		p[0] = [p[1]] + p[2]
	else:
		p[0] = []


def p_params_op(p):
	''' params_op : COMMA var_def params_op
					| empty '''
	if (len(p) == 4):
		p[0] = [p[2]] + p[3]
	else:
		p[0] = []

#! SE QUITO VARDEF

def p_bloque_func(p):
	''' bloque_func : LBRACE estatutos RBRACE'''
	p[0] =  p[2]


def p_main(p):
	''' main : MAIN LPAREN RPAREN bloque_func'''
	p[0] = p[4]


"""
#! CAMBIO DE GRAMATICA

''' var_def : VAR type_compuesto    ID ids         SEMICOLON
				| VAR type_simple   ID op_var_def  SEMICOLON '''

#! REGLA ELIMINADA                

 ''' ids : COMMA ID ids
				| empty'''

"""


def p_var_def(p):
	''' var_def :  type_compuesto    ID           
				|  type_simple       ID op_vardef   '''
	# VAR TYPE_COMP VAR1,VAR2... ;
	# VAR TYPE_SIMPLE VAR1;
	if (len(p) == 3):
		p[0] = {"type": p[1], "id": p[2]}
	else:
		p[0] = {"type": p[1], "id": p[2], "dims": p[3]}


def p_op_vardef(p):
	''' op_vardef : LBRACKET CTEI RBRACKET 
					| LBRACKET CTEI RBRACKET LBRACKET CTEI RBRACKET 
					| empty'''
	dims = []
	if(len(p) == 4):
		dims = [p[2]]
	elif (len(p) == 7):
		dims = [p[2], p[5]]
	p[0] = dims


def p_type_simple(p):
	''' type_simple : INT
					| FLOAT
					| STRING 
					| BOOL'''
	if p[0] == "int":
		return BaseType.INT
	elif p[0] == "float":
		return BaseType.FLOAT			
	elif p[0] == "bool":
		return BaseType.BOOL
	else:
		return BaseType.STRING
	
# def p_bool_true(p):
# 	''' bool : TRUE'''
# 	p[0] = True

# def p_bool_false(p):
# 	''' bool : false'''
# 	p[0] = True

def p_type_compuesto(p):
	''' type_compuesto : ID '''
	p[0] = p[1]


def p_estatutos(p):
	''' estatutos : estatuto
				| estatuto estatutos
				| empty '''
	if(len(p) == 3):
		p[0] = [p[1]]+p[2]
	else:
		if p[1] == None:
			p[0] = []
		else:
			p[0] = [p[1]]

#! SE AGREGO SEMICOLON A LLAMADA_FUNC Y LLAMADA_OBJ y VAR FEC

# Asignacion : VAR EXISTA, y no METODO, Y que el tipo expresion sea correcto
# returns : cambiar que solo las funciones puedan tener el return
# 
def p_estatuto(p):
	''' estatuto : asignacion
				| expresion
				| returns
				| llamada_funcion SEMICOLON
				| llamada_objeto SEMICOLON
				| var_def SEMICOLON
				| lectura
				| escritura
				| decision
				| repeticion '''
	p[0] = p[1]


def p_asignacion(p):
	''' asignacion : variable EQUAL expresion SEMICOLON '''
	p[0] = ("ASSIGN", p[1], p[3])


"""
#! CAMBIO DE GRAMATICA, REGLAS DE EXPRESIONES MODIFICADAS 

''' expr : expresion
			 | expresion binop expresion '''

''' expresion : termino op_expresion '''

''' op_expresion : plus_minus expresion 
					 | empty'''
	
''' termino : factor op_factor '''

''' op_factor : mulop factor
				| empty '''

''' factor : LPAREN expr RPAREN 
			| var_cte
			| variable '''
			
''' mulop : TIMES 
			  | DIVIDE '''

## ADD ESTO
	expresion : expresion BINOP expresion
			   | plus_minus expresion
			   | LPAREN expresion RPAREN
			   | var_cte     

"""


def p_expresion(p):
	''' expresion : expresion binop expresion
					| plus_minus expresion
					| LPAREN expresion RPAREN
					| var_cte '''
	if(len(p) == 2):
		p[0] = p[1]
	elif(len(p) == 3):
		p[0] = UnopNode(p[1], p[2])
	else:
		if (p[1] == '('):
			p[0] = p[2]
		else:
			p[0]=p[2](p[1], p[3]) # Cambiar por dicccionario


def p_binop(p):
	''' binop : SAME
			| NOTEQ
			| GTHAN 
			| LTHAN 
			| PLUS
			| MINUS
			| TIMES
			| DIVIDE'''
	if p[1] == '==':
		p[0] = EqualsNode
	elif p[1] == '+':
		p[0] = PlusNode
	elif p[1] == '-':
		p[0] = MinusNode
	elif p[1] == '*':
		p[0] = TimesNode
	elif p[1] == '/':
		p[0] = DivideNode
	elif p[1] == '!=':
		p[0] = NotEqualsNode
	elif p[1] == '>':
		p[0] = GTNode
	elif p[1] == '<':
		p[0] = LTNode


def p_plus_minus(p):
	''' plus_minus : PLUS
					| MINUS '''
	p[0] = p[1]


def p_var_cte(p):
	''' var_cte : variable'''
	p[0] = p[1]


def p_var_cte(p):
	''' var_cte : boolean '''
	p[0] = BoolNode(p[1])



def p_var_cte(p):
	''' var_cte : CTEF '''
	p[0] = FloatNode(p[1])


def p_var_cte(p):
	''' var_cte : CTEI '''
	p[0] = IntNode(p[1])


def p_bool(p):
	''' boolean : TRUE
				| FALSE '''
	p[0] = p[1]

def p_returns(p):
	''' returns : RETURN expresion SEMICOLON '''
	p[0] = ("RETURNS", p[2])

#! SE QUITO EL SEMICOLON


def p_llamada_funcion(p):
	''' llamada_funcion : ID LPAREN param_llamada RPAREN '''
	p[0] = ("CALL_FUNC", {"id": p[1], "params": p[3]})


"""
#! GRAMATICA CORREGIDA 

''' param_llamada : expresion
				  | empty '''

"""


def p_param_llamada(p):
	''' param_llamada : expresion
									  | expresion COMMA param_llamada
									  | empty '''
	if(len(p) == 2):
		if (p[1] == None):
			p[0] = []
		else:
			p[0] = [p[1]]
	else:
		p[0] = [p[1]] + p[3]


def p_llamada_objeto(p):
	''' llamada_objeto : ID DOT ID LPAREN param_llamada RPAREN  '''
	p[0] = ("CALL_OBJ", {"className": p[1],
						 "methodName": p[3], "params": p[5]})


def p_lectura(p):
	''' lectura : READ LPAREN variable op_lectura RPAREN SEMICOLON '''
	p[0] = ("READ", [p[3]]+p[4])


def p_op_lectura(p):
	''' op_lectura : COMMA variable op_lectura 
							   | empty '''
	if (len(p) == 2):
		p[0] = []
	else:
		p[0] = [p[2]] + p[3]

#! SE AGREGO LLAMADA OBJETO


def p_variable(p):
	''' variable : ID variable_op
				| llamada_objeto '''
	if(len(p) == 3):
		p[0] = VarCallNode( p[1],  p[2])
	else:
		p[0] = p[1]


def p_variable_op(p):
	''' variable_op : DOT ID 
					| LBRACKET expresion RBRACKET 
					| LBRACKET expresion RBRACKET LBRACKET expresion RBRACKET
					| empty
									'''
	if(len(p) == 2):
		if(p[1] == None):
			p[0] = ("Simple")
		else:
			p[0] = ("method_call", p[1])
	elif (len(p) == 3):
		p[0] = ("attribute_call", p[2])
	elif (len(p) == 4):
		p[0] = ("Array", p[2])
	else:
		p[0] = ("MATRIX", (p[2], p[5]))


"""
#! GRAMATICA MODIFICADA

variable_op : DOT ID
					| LBRACKET expresion RBRACKET matrix
					| empty
					
GRAMATICA ELIMINADA

matrix : LBRACKET expresion RBRACKET
			   | empty

"""


def p_escritura(p):
	''' escritura : WRITE LPAREN type_escritura op_escritura RPAREN SEMICOLON '''
	p[0] = ("WRITE", [p[3]] + p[4])


def p_type_escritura(p):
	''' type_escritura : CTESTRING 
									   | expresion '''
	p[0] = p[1]


def p_op_escritura(p):
	''' op_escritura : COMMA CTESTRING op_escritura 
									 | COMMA expresion op_escritura
									 | empty '''
	if(len(p) == 4):
		p[0] = [p[2]]
	else:
		p[0] = []


def p_decision(p):
	''' decision : IF LPAREN expresion RPAREN THEN LBRACE estatutos RBRACE op_decision '''
	p[0] = ("IF_STMT", {"condition": p[3], "estatutos": p[7], "else": p[9]})


def p_op_decision(p):
	''' op_decision : ELSE LBRACE estatutos RBRACE 
									| empty '''
	if(len(p) == 4):
		p[0] = [p[3]]
	else:
		p[0] = []


def p_repeticion(p):
	''' repeticion : condicional 
							   | no_condicional '''
	p[0] = p[1]


def p_condicional(p):
	''' condicional : WHILE LPAREN expresion RPAREN DO LBRACE estatutos RBRACE '''
	p[0] = ("WHILE", {"condition": p[3], "estatutos": p[7]})


def p_no_condicional(p):
	''' no_condicional : FROM variable EQUAL expresion TO expresion DO LBRACE estatutos RBRACE '''
	p[0] = ("FOR", {"VAR": p[2], "ASSIGN": p[4], "END": p[6], "BODY": p[9]})


"""
#! CAMBiO GRAMATICA QUITAR TYPE NO CONDICIONAL

type_no_condicional : ID.ID
	| ID LBRACKET expresion RBRACKET 
	| ID LBRACKET expresion RBRACKET LBRACKET expresion RBRACKET

"""


def p_empty(p):
	''' empty : '''
	p[0] = None


def p_error(p):
	print("Syntax error in input!")


precedence = (
	('left', 'PLUS', 'MINUS'),
	('left', 'TIMES', 'DIVIDE'),
)

parser = yacc.yacc()

programa_ejemplo = '''

int alan ; 

Clase team{
	int cool;
	Funcion electron(){
		
	}
}

Funcion karen(int alanbruki, int bo) -> int 
{
	
}

Main ()
{
	alan = 4; 
	lee ( alan.cabello , alan );
	i = 3*3-1/-(alan+b); 
	hola(i.hola);
	desde i = 1 hasta 10 hacer 
	{ 
		escribe("hola", 10);
	}
}
 '''  # FUNCIONO!


print(parser.parse(programa_ejemplo))

# print(parser.parse(programa_ejemplo+";")) ##ERROR
SemanticAnalyzer(programa_ejemplo).analisis_semantico("codigo.pkl")