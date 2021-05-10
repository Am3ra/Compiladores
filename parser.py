import ply.yacc as yacc
import pickle
from lexer import lexer
from lexer import tokens
from enum import Enum
import pprint
# from semanticAnalyzer import 

#! TIPOS DISPONIBLES EN EL LENGUAJE:
# 1) TIPOS SIMPLES
# 2) LOS KEYS DE LA TABLA DE CLASES 

# simple_types + symbol_table_classes.keys()


#! Juntar simbolos?


class SemanticAnalyzer():
	def __init__(self, input=None, debug = False):
		if input is not None:
			self.input = input
			self.parser = yacc.yacc()
			self.main: MainNode = self.parser.parse(input)
		self.symbol_table_list = [{}]


	def analisis_semantico(self,filename="a.out",debug=False):
		#Falta hacer el analysis
		if debug:
			print(self.main)

		self.main.analyze(self)

		
		
		if filename is not None:
			f = open(filename,'wb')
			pickle.dump(self.main,f) # Se serializa el AST
			f.close()

	def declarar_class(self, dec):
		self.check_if_declared_global(dec, "CLASS")
		self.symbol_table_classes[dec["id"]] = dec

	
	def declare_symbol_class(self, dec, class_name, type):
		# self.check_if_declared_class(self,dec,class_name)
		check_if_symbol_declared_scope(dec,self.symbol_table_classes[class_name])
		self.symbol_table_classes[class_name][type][dec["id"]] = dec

def declarar_symbol_scopes(dec,scopes : [dict]):
	''' takes a declaration of any type (class, varaible, function) and 
		checks if already declared in current and global scope. \n
		`raise`s `SemanticError` if already declared \n
		insert at the end of current `scope` if not declared'''
	if (check_if_symbol_declared_scopes(dec["id"],scopes)):
		raise SemanticError("{0} already declared".format(dec["id"]))
	scopes[-1][dec["id"]] = dec

def check_if_symbol_declared_scopes(id : str,scopes:[dict]):
	''' takes a string id, list of dicts\n
		returns declaration if found.\n
		returns `False` if not '''
	for scope in reversed(scopes):
		if (scope.get(id) is not None):
			return scope.get(id)
	return False
	
def declarar_symbol_scopes_run(dec, scopes, globals):
	if len(scopes) == 0:
		globals[dec["id"]] = dec
	else:
		scopes[-1][-1]["id"] = dec 

def run_lista_estatutos(vm,lista_estatutos):
	for estatuto in lista_estatutos:
		if isinstance(estatuto, ReturnNode):
			return estatuto.run(vm)
		estatuto.run(vm)
		
# SemanticAnalyzer(text).analisis_semantico()

class Node():
	'''Generic Class interface'''
	def analyze(self, analyzer: SemanticAnalyzer):
		'''Complete Semantic analysis of this node '''
		pass

	def run(self, vm):
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
	
	def run(self, vm):
		for dec  in self.declaraciones:
			dec.run(vm)

		vm.symbol_scope_list+= [{}]		
		for estatuto in self.main:
			if isinstance(estatuto, ReturnNode):
					return estatuto.run(vm)
			estatuto.run(vm)

	
	def __repr__(self):
		return pprint.pformat(("Programa", self.declaraciones, self.main),indent=1)	


class VarDecNode(Node):
	def __init__(self, dec):
		self.dec = dec


	def __repr__(self):
		return pprint.pformat(("VARDEC", self.dec))

	def analyze(self, analyzer: SemanticAnalyzer):
		# print("Symbol list:",analyzer.symbol_table_list)
		declarar_symbol_scopes(self.dec,analyzer.symbol_table_list)

	def run(self,vm):
		declarar_symbol_scopes_run(self.dec,vm.symbol_scope_list,vm.global_symbols)

class FuncDecNode(Node):
	def __init__(self, dec):
		self.dec = dec
		#{"name": p[2], "params": p[4], "return_op": p[6],
		# ""estatutos": p[7]}

	def __repr__(self):
		return pprint.pformat(("FUNCDEC", self.dec))

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
				if  isinstance(estatuto, ReturnNode): # PseudoCode
					if estatuto.analyze(analyzer) != self.dec["return_op"]:
						raise SemanticError("Return of Wrong Type!")
					else:
						break
			else:
				raise SemanticError("Function is Missing Return!")
		
		# print(analyzer.symbol_table_list)

		analyzer.symbol_table_list.pop()

	def run(self,vm):
		declarar_symbol_scopes_run(self.dec,vm.symbol_scope_list,vm.global_symbols)

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

	def __repr__(self):
		return pprint.pformat(("CLASSDEC", self.dec))

	def analyze(self, analyzer: SemanticAnalyzer):
		# Checar que si existe la herencia

		
		# Checar el id
		if check_if_symbol_declared_scopes(self.dec["id"],analyzer.symbol_table_list):
			raise SemanticError("Clase ya declarada")
		# Checar nombres de funcs y vars
		analyzer.symbol_table_list[0][self.dec["id"]] = ({"id": self.dec["id"],"attributes":self.dec["attributes"],"methods":self.dec["methods"]})

		scope = [{}]

		for attribute in self.dec["attributes"] :
			declarar_symbol_scopes(attribute.dec, scope)

		for method in self.dec["methods"] :
			declarar_symbol_scopes(method, scope)

		## Agregar cosas inheritance
		# print(declarar_symbol_scopes)

		if (self.dec["inheritance"]):
			father = analyzer.symbol_table_list[0].get(self.dec["inheritance"])
			if (father is None):
				raise SemanticError("Inherits undeclared class")
			else:
				for attribute in father["attributes"]:
					analyzer.symbol_table_list[0][self.dec["id"]]["attributes"].setdefault(attribute,father[attribute])

	def run(self,vm):
		scope = [{}]

		for attribute in self.dec["attributes"] :
			declarar_symbol_scopes_run(attribute, scope,None)

		for method in self.dec["methods"] :
			declarar_symbol_scopes_run(method, scope, None)
		declarar_symbol_scopes_run(self.dec,vm.symbol_scope_list,vm.global_symbols)


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
	'''
	Takes a `VarCallNode` and an `Expression`
	check that variable exists, and is same type as expression.
	assignes true to `"defined"` field of var dec
	'''
	def __init__(self, var, expresion):
		self.var = var
		self.expresion = expresion



	def __repr__(self):
		return pprint.pformat(("ASSIGN", self.var, self.expresion))

	def analyze(self, analyzer: SemanticAnalyzer):
		
		var_type = self.var.analyze(analyzer,True)
		expr_type = self.expresion.analyze(analyzer)

		if var_type is not expr_type:
			raise SemanticError("Wrong types in assign: Found {1}, expected:{0}".format(var_type,expr_type))
		
		check_if_symbol_declared_scopes(self.var.id,analyzer.symbol_table_list)["defined"] = True
		

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


	def __repr__(self):
		return pprint.pformat(("UNOP", self.operation, self.operand))

	def analyze(self, analyzer: SemanticAnalyzer):
		operand_type = self.operand.analyze()

		if operand_type is not BaseType.INT or operand_type is not BaseType.FLOAT:
			SemanticError("Can only apply unary +/- to int or float")
		else:
			return operand_type
	
	def run(self,vm):
		if self.operation == '+':
			return self.operand.run(vm)
		else :
			return - self.operand.run(vm)

#done
class BinopNode(Node):
	def __init__(self, lhs, rhs):
		self.lhs = lhs
		self.rhs = rhs

	def __repr__(self):
		return pprint.pformat(("BINOP", self.lhs, self.rhs))

	def analyze(self, analyzer: SemanticAnalyzer):
		lh_type = self.lhs.analyze(analyzer)
		rh_type = self.rhs.analyze(analyzer)

		if lh_type is BaseType.STRING:
			raise SemanticError("Strings cannot be used in binary operations")

		if lh_type is BaseType.BOOL:
			raise SemanticError("Booleans cannot be used in binary operations")

		if lh_type != rh_type:
			raise SemanticError("Binary operations can only be done with same types")
		else:
			return lh_type

class CompareNode(BinopNode):
	def analyze(self, analyzer):
		lh_type = self.lhs.analyze(analyzer)
		rh_type = self.rhs.analyze(analyzer)
		
		if lh_type is BaseType.STRING:
			raise SemanticError("Strings cannot be used in binary operations")

		if lh_type != rh_type:
			raise SemanticError("Binary operations can only be done with same types")
		else:
			return BaseType.BOOL

class PlusNode(BinopNode):
	

	def __repr__(self):
		return "{0}".format(("PLUS",self.lhs, self.rhs))

	def run(self,vm):
		lhs = self.lhs.run(vm)
		rhs = self.rhs.run(vm)

		return lhs + rhs

	# def compile(self,vm):
	# 	lhs = self.lhs.run(vm)
	# 	rhs = self.rhs.run(vm)
	# 	current_pos = vm.current_pos()
	# 	print("+ {0} {1} {2}".format(lhs,rhs,current_pos))
	# 	return current_pos
	

class MinusNode(BinopNode):


	def __repr__(self):
		return pprint.pformat(("MINUS",  self.lhs, self.rhs))
		
	def run(self,vm):
		lhs = self.lhs.run(vm)
		rhs = self.rhs.sun(vm)

		return lhs - rhs

class TimesNode(BinopNode):
	

	def __repr__(self):
		return pprint.pformat(("TIMES", self.lhs, self.rhs))
	
	def run(self,vm):
		lhs = self.lhs.run(vm)
		rhs = self.rhs.sun(vm)

		return lhs * rhs

class DivideNode(BinopNode):

	def __repr__(self):
		return pprint.pformat(("DIVIDE",  self.lhs, self.rhs))
		
	def run(self,vm):
		lhs = self.lhs.run(vm)
		rhs = self.rhs.sun(vm)

		return lhs / rhs

class EqualsNode(CompareNode):
	
	def __repr__(self):
		return pprint.pformat(("EQUALS", self.lhs, self.rhs))
	
	def run(self,vm):
		lhs = self.lhs.run(vm)
		rhs = self.rhs.sun(vm)

		return lhs == rhs

class NotEqualsNode(CompareNode):
	

	def __repr__(self):
		return pprint.pformat(("NOTEQ",  self.lhs, self.rhs))
	
	def run(self,vm):
		lhs = self.lhs.run(vm)
		rhs = self.rhs.sun(vm)

		return lhs != rhs

class GTNode(CompareNode):
	

	def __repr__(self):
		return pprint.pformat(("GTHAN",  self.lhs, self.rhs))

	def run(self,vm):
		lhs = self.lhs.run(vm)
		rhs = self.rhs.sun(vm)

		return lhs > rhs

class LTNode(CompareNode):


	def __repr__(self):
		return pprint.pformat(("LTHAN",  self.lhs, self.rhs))
	
	def run(self,vm):
		lhs = self.lhs.run(vm)
		rhs = self.rhs.sun(vm)

		return lhs < rhs

class ConstantNode(Node):

	def analyze(self,  analyzer):
		return self.type_name
		


	def __repr__(self):
		return pprint.pformat(("CONSTANT",  self.value, self.type_name))
	
	def run(self, vm):
		return self.value



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

class StringNode(ConstantNode):
	def __init__(self, value):
		self.value = value
		self.type_name = BaseType.STRING

class VarCallNode(Node):
	'''
	Takes a `String` id, and a `BaseType` type.\n
	Checks if variable is declared, and that call is correct.\n
	Returns `type` of var
	
	'''
	def __init__(self,id,call_type):
		self.id = id
		self.call_type = call_type
	
	def __repr__(self):
		return pprint.pformat(("VAR_CALL", self.id, self.call_type))
		
	def analyze(self, analyzer, assignment=False, var = None):
		if var is None:
			scope = analyzer.symbol_table_list
		else:
			scope = [var["scope"]] # revisar el padre 
		# Checar que existe
		var = check_if_symbol_declared_scopes(self.id,scope)
		## CHECK CALL TYPE IS THE SAME AS VAR DIMS
		if var:
			if not assignment:
				if var["defined"]:
					if self.call_type is None:
						return var["type"]
					return self.call_type.analyze(analyzer,var = var)
				else:
					raise SemanticError("CAN'T CALL UNDEFINDED VAR {0}".format(self.id))
			else:
				var["defined"] == True
				if self.call_type is None:
					return var["type"]
				return self.call_type.analyze(analyzer, var = var)
		else:
			raise SemanticError("CAN'T CALL UNDECLARED VAR {0}".format(self.id))

	def run(self, vm, assignment = False):
		var = check_if_symbol_declared_scopes(self.id,[vm.global_symbols]+vm.symbol_scope_list[-1])

		var_space = self.call_type.run(var, vm)
		if assignment:
			var_space["value"] = assignment
		else:
			return var_space["value"]


class SimpleCallNode(Node):
	def __init__(self,dims):
		self.dims = dims

	def analyze(self,analyzer : SemanticAnalyzer,var):
		if var["symbol_type"] != "simple":
			raise SemanticError("Expected simple var.\n Recieved: {0}".format(var["symbol_type"]))

		if len(var["dims"]) != len(self.dims):
			return SemanticError("Wrong number of Dimensions! \n Expected: {0}".format(var["dims"]))
		for dim in self.dims:
			dimtype = dim.analyze()

			if dimtype is not BaseType.INT:
				return SemanticError("Index has to be int, found  {0}".format(dimtype))

		return var["type"]

	def run(self, var, vm):
		for (dimcall,dimVar) in zip(self.dims,var["dims"]):
			dimcall = dimcall.run(vm)
			if dimcall >= dimVar:
				raise RuntimeError("Index out of bounds! Max index: {0}, recieved: {1}".format(dimVar,dimcall))
		current_val = var["value"]
		for dim in current_val:
			current_val = current_val[dim]
		return current_val


class MethodCallNode():
	pass

class AttributeCallNode():	
	'''Attribute call node analyzes and executes attribute calls.\n
	Take a var and an attribute name'''
	def __init__(self, attributeName):
		self.attributeName = attributeName
	
	def __repr__(self):
		return pprint.pformat(("ATTRIBUTE CALL", self.var, self.attributeName))

	def analyze(self,var,analyzer:SemanticAnalyzer):
		# Does attribute exist?
		if var["symbol_type"] != "object":
			raise SemanticError("Expected object var.\n Recieved: {0}".format(var["symbol_type"]))

		if len(var["scope"][self.attributeName]["dims"]) != len(self.dims):
			return SemanticError("Wrong number of Dimensions! \n Expected: {0}".format(var["dims"]))
		for dim in self.dims:
			dimtype = dim.analyze()

			if dimtype is not BaseType.INT:
				return SemanticError("Index has to be int, found  {0}".format(dimtype))

		return var["type"]



#hDONE
class ReturnNode(Node):
	'''
	Return node analyzes an expresion recieved and executes it\n 
	takes an expresion
	'''
	def __init__(self, expr):
		self.expr = expr


	def __repr__(self):
		return pprint.pformat(("RETURN", self.expr))

	def analyze(self, analyzer: SemanticAnalyzer):
		return self.expr.analyze(analyzer)
	
	def run(self,vm):
		return self.expr.run(vm)

class FuncCallNode(Node):
	def __init__(self, dec):
		self.dec = dec


	def __repr__(self):
		return pprint.pformat(("VARDEC", self.dec))

	def analyze(self, analyzer: SemanticAnalyzer):
		pass
		
class ObjectCallNode(Node):
	def __init__(self, dec):
		self.dec = dec


	def __repr__(self):
		return pprint.pformat(("VARDEC", self.dec))

	def analyze(self, analyzer: SemanticAnalyzer):
		pass

class ReadNode(Node):
	''' Readnode takes an array of VarCallNodes names as a parameter.\n
		Reads series of inputs into vars, makes them defined.\n
		Returns nothing.\n
		Raises `SemanticError` if var not declared '''
	def __init__(self, variables : [VarCallNode]):
		self.variables = variables


	def __repr__(self):
		return pprint.pformat(("READ", self.variables))

	def analyze(self, analyzer: SemanticAnalyzer):
		for var in self.variables:
			var = check_if_symbol_declared_scopes(var.id,analyzer.symbol_table_list)
			if not var:
				raise SemanticError("Can't read into variable that's not declared")
			if var["type"] is not BaseType.STRING:
				raise SemanticError("Can only read into String type var")
			var["defined"] = True

	def run(self, vm):
		for var in self.variables:
			# obtener variable
			var = check_if_symbol_declared_scopes(var.id,[vm.global_symbols]+vm.symbol_scope_list[-1][-1])
			# obtener input()
			# escribir resultado de input() en el valor de la variable
			var["value"] = input()

class WriteNode(Node):
	'''
	Takes a list of expresions, writes them to console.
	
	'''
	def __init__(self, expresiones):
		self.expresiones = expresiones 


	def __repr__(self):
		return pprint.pformat(("WRITE", self.expresiones))

	def analyze(self, analyzer: SemanticAnalyzer):

		for expresion in self.expresiones:
			expresion.analyze(analyzer)

	def run(self, vm):
		for expresion in self.expresiones:
			print(expresion.run(vm))
		
class IfNode(Node):
	'''
	Takes a condition, a body and sometimes and else_body \n
	Evaluates condition and checks if evaluation is `BaseType.BOOL` and if not `raises` `SemanticError`,
	Then analyzes `estatutos` in `body`,
	Then analyzes `estatutos` in `else_body`
	'''
	def __init__(self, condition, body, else_body):
		self.condition = condition
		self.body = body
		self.else_body = else_body
		

	def __repr__(self):
		return pprint.pformat(("IfNode", self.condition, self.body, self.else_body))

	def analyze(self, analyzer: SemanticAnalyzer):
		# print("Symbol list:",analyzer.symbol_table_list)
		# Checar que expresion condicion sea bool
		condition_type = self.condition.analyze(analyzer)
		if condition_type is not BaseType.BOOL:
			raise SemanticError("Condition has to return BOOL type")
		
		for estatuto in self.body:
			estatuto.analyze(analyzer)
		
		for estatuto in self.else_body:
			estatuto.analyze(analyzer)

	def run(self,vm):
		if self.condition == True:
			for estatuto in self.body:
				if isinstance(estatuto, ReturnNode):
					return estatuto.run(vm)
				estatuto.run(vm)
		else:
			for estatuto in self.else_body:
				if isinstance(estatuto, ReturnNode):
					return estatuto.run(vm)
				estatuto.run(vm)


class WhileNode(Node):
	'''
	Takes a condition and a body.\n 
	evaluates condition and checks if evaluation is `BaseType.BOOL` and if not `raises` `SemanticError`,
	then analyzes `estatutos` in `body`,
	
	'''
	def __init__(self, condition, body):
		self.condition = condition
		self.body = body


	def __repr__(self):
		return pprint.pformat(("WHILE", self.condition, self.body))

	def analyze(self, analyzer: SemanticAnalyzer):
		condition_type = self.condition.analyze(analyzer)
		if condition_type is not BaseType.BOOL:
			raise SemanticError("Condition has to return BOOL type")
		for estatuto in self.body:
			estatuto.analyze(analyzer)
	
	def run(self,vm):
		while self.condition.run():
			for estatuto in self.body:
				if isinstance(estatuto, ReturnNode):
					return estatuto.run(vm)
				estatuto.run(vm)


class ForLoopNode(Node):
	'''
	`ForLoopNode` takes a control var, an assignment, a end point, and a body.\n
	Runs body while condition is true.
	'''
	def __init__(self, variable, expresion, end, body):
		self.variable = variable
		self.expresion = expresion
		self.end = end
		self.body = body


	def __repr__(self):
		return pprint.pformat(("FOR_LOOP", self.dec))

	def analyze(self, analyzer: SemanticAnalyzer):

		AssignNode(self.variable,self.expresion).analyze(analyzer)

		var_type = check_if_symbol_declared_scopes(self.variable.id,analyzer.symbol_table_list)["type"]
		if var_type is not BaseType.INT:
			raise SemanticError("Can only use ints in for loop")
		end_type = self.end.analyze(analyzer)
		
		if end_type is not BaseType.INT:
			raise SemanticError("Can only use type INT in for loop")
		
		for estatuto in self.body:
			estatuto.analyze(analyzer)

	def run(self,vm):
		var = check_if_symbol_declared_scopes(var.id,[vm.global_symbols]+vm.symbol_scope_list[-1][-1])
		var["value"] = self.expresion.run(vm)
		end = self.end.run(vm)
		while var["value"] != end:
			for estatuto in self.body:
				if isinstance(estatuto, ReturnNode):
					return estatuto.run(vm)
				estatuto.run(vm)

def generic_error(type,p):
	print("Error in {2}  on line {0} \n At index {1}".format(p.lineno(4), p.lexpos(4),type))

def p_programa(p):
	'''programa : declaraciones main '''
	p[0] = MainNode(p[1], p[2])
	

def p_declaraciones(p):
	'''declaraciones : empty '''
	p[0] = []


def p_declaraciones_variables(p):
	'''declaraciones : var_dec SEMICOLON declaraciones '''
	p[0] = [p[1]] + p[3]


def p_declaraciones_funciones(p):
	'''declaraciones : funcion_def declaraciones '''
	p[0] = [FuncDecNode(p[1])] + p[2]


def p_declaraciones_clases(p):
	'''declaraciones : clase_def declaraciones '''
	p[0] = [ClassDecNode(p[1])] + p[2]


def p_clase_def(p):
	'''clase_def : CLASS ID clase_op bloque_clase'''
	p[0] = ({"id" : p[2], "inheritance" : p[3], 
		"attributes": p[4]["attributes"], "methods" : p[4]["methods"], "symbol_type":"class"})


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
			"body":p[7], "symbol_type":"func"}


def p_op_var(p):
	''' op_var : var_dec SEMICOLON op_var
			   | empty'''
	if (len(p)==4):
		p[0] = [p[1]] + p[3]
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
	''' params : var_dec params_op
				| empty'''
	if(len(p) == 3):
		p[0] = [p[1]] + p[2]
	else:
		p[0] = []


def p_params_op(p):
	''' params_op : COMMA var_dec params_op
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


def p_main_error(p):
	''' main : MAIN LPAREN RPAREN error'''
	generic_error("main function",p)

"""
#! CAMBIO DE GRAMATICA

''' var_def : VAR type_compuesto    ID ids         SEMICOLON
				| VAR type_simple   ID op_var_def  SEMICOLON '''

#! REGLA ELIMINADA                

 ''' ids : COMMA ID ids
				| empty'''

"""


def p_var_dec(p):
	''' var_dec :  type_compuesto    ID           
				|  type_simple       ID op_vardef   '''
	# VAR TYPE_COMP VAR1,VAR2... ;
	# VAR TYPE_SIMPLE VAR1;
	if (len(p) == 3):
		p[0] = ({"type": p[1], "id": p[2], "defined": False,"symbol_type":"compound"})
	else:
		p[0] = VarDecNode({"type": p[1], "id": p[2], "dims": p[3] , "defined":False, "symbol_type":"simple"})


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
	if p[1] == "int":
		p[0] = BaseType.INT
	elif p[1] == "float":
		p[0] = BaseType.FLOAT
	elif p[1] == "bool":
		p[0] = BaseType.BOOL
	else:
		p[0] = BaseType.STRING
	
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

#! Se elimino expresion de estatutos
def p_estatuto(p):
	''' estatuto : asignacion SEMICOLON
				| expresion SEMICOLON
				| returns SEMICOLON
				| llamada_funcion SEMICOLON
				| llamada_metodo SEMICOLON
				| var_dec SEMICOLON
				| lectura SEMICOLON
				| escritura SEMICOLON
				| decision SEMICOLON
				| repeticion SEMICOLON
				 '''
	p[0] = p[1]

# def p_estatuto_returns(p):
# 	''' estatuto : asignacion 
# 				| expresion 
# 				| returns 
# 				| llamada_funcion 
# 				| llamada_metodo 
# 				| var_def 
# 				| lectura 
# 				| escritura 
# 				| decision 
# 				| repeticion '''
# 	p[0] = ReturnNode(p[1])
#  se tendria que cambiar el analisis de Return node para aceptar estatutos

def p_asignacion(p):
	''' asignacion : variable EQUAL expresion '''
	p[0] =  AssignNode(p[1], p[3])


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


def p_var_cte_var(p):
	''' var_cte : variable'''
	p[0] = p[1]


def p_var_cte_bool(p):
	''' var_cte : boolean '''
	p[0] = BoolNode(p[1])



def p_var_cte_f(p):
	''' var_cte : CTEF '''
	p[0] = FloatNode(p[1])


def p_var_cte_i(p):
	''' var_cte : CTEI '''
	p[0] = IntNode(p[1])

def p_var_cte_string(p):
	''' var_cte : CTESTRING'''
	p[0] = StringNode(p[1])


def p_bool(p):
	''' boolean : TRUE
				| FALSE '''
	p[0] = p[1]

def p_returns(p):
	''' returns : RETURN expresion '''
	p[0] = ReturnNode(p[2])

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


def p_llamada_metodo(p):
	''' llamada_metodo : ID DOT ID LPAREN param_llamada RPAREN  '''
	p[0] = ("CALL_OBJ", {"objectName": p[1],
						 "methodName": p[3], "params": p[5]})


def p_lectura(p):
	''' lectura : READ LPAREN variable op_lectura RPAREN '''
	p[0] = ReadNode([p[3]]+p[4])


def p_op_lectura(p):
	''' op_lectura : COMMA variable op_lectura 
					| empty '''
	if (len(p) == 2):
		p[0] = []
	else:
		p[0] = [p[2]] + p[3]

#! Se quito llamada objeto


def p_variable(p):
	''' variable : ID variable_op '''
	p[0] = VarCallNode( p[1],  p[2])


def p_variable_op(p):
	''' variable_op : DOT variable
					| LBRACKET expresion RBRACKET 
					| LBRACKET expresion RBRACKET LBRACKET expresion RBRACKET
					| empty
									'''
	if(len(p) == 2):
		p[0] =	SimpleCallNode([])
	elif (len(p) == 3):
		p[0] = p[2]
	elif (len(p) == 4):
		p[0] = SimpleCallNode([p[2]])
	else:
		p[0] = SimpleCallNode([p[2], p[5]])

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
	''' escritura : WRITE LPAREN expresion op_escritura RPAREN '''
	p[0] = WriteNode([p[3]] + p[4])


def p_op_escritura(p):
	''' op_escritura : COMMA expresion op_escritura
					| empty '''
	if(len(p) == 4):
		p[0] = [p[2]]
	else:
		p[0] = []


def p_decision(p):
	''' decision : IF LPAREN expresion RPAREN LBRACE estatutos RBRACE op_decision '''
	p[0] = IfNode(p[3],p[6], p[8])


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
	p[0] = WhileNode(p[3], p[7])


def p_no_condicional(p):
	''' no_condicional : FROM variable EQUAL expresion TO expresion DO LBRACE estatutos RBRACE '''
	p[0] = ForLoopNode(  p[2], p[4],  p[6], p[9])


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
	raise SyntaxError("Syntax error in input!")

precedence = (
	('left', 'PLUS', 'MINUS'),
	('left', 'TIMES', 'DIVIDE'),
)




