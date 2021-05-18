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

''' 
El manejo de memoria es de maner dinamica, por lo cual no se especificaran 
registros en memoria de manera estática
'''
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
	
def declarar_symbol_scopes_run(dec, scopes, globals,force=False):
	if force:
		scopes[-1][dec["id"]] = dec
	elif len(scopes) == 1 and len(scopes[0]) == 0:
		globals[dec["id"]] = dec
	else:
		scopes[-1][-1][dec["id"]] = dec 

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

		return self.main.analyze(analyzer)
	
	def run(self, vm):
		for dec  in self.declaraciones:
			dec.run(vm)

		
		return self.main.run(vm)

	
	def __repr__(self):
		return pprint.pformat(("Programa", self.declaraciones, self.main),indent=1)	


class VarDecNode(Node):
	def __init__(self, dec, lineno = None):
		self.dec = dec
		self.lineno = lineno

	def __repr__(self):
		return pprint.pformat(("VARDEC", self.dec))

	def analyze(self, analyzer: SemanticAnalyzer):
		# print("Symbol list:",analyzer.symbol_table_list)
		declarar_symbol_scopes(self.dec,analyzer.symbol_table_list)

	def run(self,vm):
		self.dec["value"] = [] 
		declarar_symbol_scopes_run(self.dec,vm.symbol_scope_list,vm.global_symbols)

class FuncDecNode(Node):
	def __init__(self, dec, lineno = None):
		self.dec = dec
		self.lineno = lineno
		#{"name": p[2], "params": p[4], "return_op": p[6],
		# ""estatutos": p[7]}

	def __repr__(self):
		return pprint.pformat(("FUNCDEC", self.dec))

	def analyze(self, analyzer: SemanticAnalyzer):
		## CHECAR ID GLOBAL
		if (check_if_symbol_declared_scopes(self.dec["id"], analyzer.symbol_table_list) ):
			raise SemanticError("Symbol declared with same name.",self.lineno)


		# print(analyzer.symbol_table_list)

		## CREAR DIC VACIO
		analyzer.symbol_table_list[0][self.dec["id"]] = self.dec

		analyzer.symbol_table_list.append({})
		# print("push to list")
		# print(analyzer.symbol_table_list)

		#Declarar todos los params

		## DECLARAR PARAMETROS
		for param in self.dec["params"]:
			param.analyze(analyzer)
		
		var = self.dec["body"].analyze(analyzer)
		# for estatuto in self.dec["body"]:
		# 	estatuto.analyze(analyzer)
		# ## Analyzar CUERPO
		# if has return type

			
		if var != self.dec["return_op"]:
			raise SemanticError("Return of Wrong Type! \nExpected:{0}\nRecieved:{1}".format(self.dec["return_op"],var),self.lineno)
				
		
		print(analyzer.symbol_table_list)

		analyzer.symbol_table_list.pop()
		# print(analyzer.symbol_table_list)



	def run(self,vm):
		declarar_symbol_scopes_run(self.dec,vm.symbol_scope_list,vm.global_symbols)

		# print(analyzer.symbol_table_list)

class SemanticError(Exception):
	def __init__(self, message, lineno = None):
		self.lineno = "" if lineno is None else "Error on line {}!\n".format(lineno)
		self.message = message
		super().__init__(self.lineno+self.message)

class ClassDecNode(Node):
	def __init__(self, dec, lineno = None):
		self.dec = dec
		self.lineno = lineno
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
			raise SemanticError("Clase ya declarada",self.lineno)
		# Checar nombres de funcs y vars
		analyzer.symbol_table_list[0][self.dec["id"]] = ({"id": self.dec["id"],"attributes":self.dec["attributes"],"methods":self.dec["methods"],"symbol_type": "class"})
		analyzer.symbol_table_list[0][self.dec["id"]]["scope"] = [{}]
		scope = analyzer.symbol_table_list[0][self.dec["id"]]["scope"] 

		for attribute in self.dec["attributes"] :
			declarar_symbol_scopes(attribute.dec, scope)

		for method in self.dec["methods"] :
			declarar_symbol_scopes(method.dec, scope)

		## Agregar cosas inheritance
		# print(declarar_symbol_scopes)

		if (self.dec["inheritance"]):
			father = analyzer.symbol_table_list[0].get(self.dec["inheritance"])
			if (father is None):
				raise SemanticError("Inherits undeclared class",self.lineno)
			else:
				for attribute in father["attributes"]:
					analyzer.symbol_table_list[0][self.dec["id"]]["attributes"].setdefault(attribute,father[attribute])

	def run(self,vm):
		scope = [{}] ##

		for attribute in self.dec["attributes"] :
			declarar_symbol_scopes_run(attribute.dec, scope,None,force=True)

		for method in self.dec["methods"] :
			declarar_symbol_scopes_run(method.dec, scope, None,force=True)

		self.dec["scope"] = scope
		declarar_symbol_scopes_run(self.dec,vm.symbol_scope_list,vm.global_symbols)


class BloqueNode(Node):
	def __init__(self,  estatutos, lineno = None):
		self.estatutos = estatutos
		self.lineno = lineno

	def __str__(self):
		return "{0}".format(("BLOQUE CODE", self.estatutos))

	def __repr__(self):
		return "{0}".format(("BLOQUE CODE", self.estatutos))

	def analyze(self, analyzer: SemanticAnalyzer):
		analyzer.symbol_table_list.append({})# Push new lexical scope


		for estatuto in self.estatutos:
			if isinstance(estatuto, ReturnNode):
				a = estatuto.analyze(analyzer)
				analyzer.symbol_table_list.pop() # pop lexical scope
				return a
			estatuto.analyze(analyzer)

		# print("BloqueFUNC",analyzer.symbol_table_list)
		# del analyzer.symbol_table_list[-1]
		# analyzer.symbol_table_list.pop() # pop lexical scope
		analyzer.symbol_table_list.pop() # pop lexical scope

	def run(self,vm):
		vm.symbol_scope_list[-1].append({}) 

		for estatuto in self.estatutos:
			if isinstance(estatuto, ReturnNode) :
				a = estatuto.run(vm)
				vm.symbol_scope_list[-1].pop()
				return a
			elif isinstance(estatuto,IfNode):
				a = estatuto.run(vm)
				if a is not None:
					vm.symbol_scope_list[-1].pop()
					return a
			estatuto.run(vm)


		vm.symbol_scope_list[-1].pop()

class AssignNode(Node):
	'''
	Takes a `VarCallNode` and an `Expression`
	check that variable exists, and is same type as expression.
	assignes true to `"defined"` field of var dec
	'''
	def __init__(self, var, expresion, lineno = None):
		self.var = var
		self.expresion = expresion
		self.lineno = lineno


	def __repr__(self):
		return pprint.pformat(("ASSIGN", self.var, self.expresion))

	def analyze(self, analyzer: SemanticAnalyzer):
		
		expr_type = self.expresion.analyze(analyzer)
		var_type = self.var.analyze(analyzer,True)

		if var_type is not expr_type:
			raise SemanticError("Wrong types in assign: Found {1}, expected:{0}".format(var_type,expr_type),self.lineno)
		
		check_if_symbol_declared_scopes(self.var.id,analyzer.symbol_table_list)["defined"] = True

	def run(self,vm):
		assignment = self.expresion.run(vm)
		self.var.run(vm,assignment)
		

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
	def __init__(self, lhs, rhs, lineno = None):
		self.lhs = lhs
		self.rhs = rhs
		self.lineno = lineno

	def __repr__(self):
		return pprint.pformat((self.__class__.__name__, self.lhs, self.rhs))

	def analyze(self, analyzer: SemanticAnalyzer):
		lh_type = self.lhs.analyze(analyzer)
		rh_type = self.rhs.analyze(analyzer)

		if lh_type is BaseType.STRING:
			raise SemanticError("Strings cannot be used in binary operations",self.lineno)

		if lh_type is BaseType.BOOL:
			raise SemanticError("Booleans cannot be used in binary operations",self.lineno)

		if lh_type != rh_type:
			raise SemanticError("Binary operations can only be done with same types",self.lineno)
		else:
			return lh_type

class CompareNode(BinopNode):

	def analyze(self, analyzer, lineno = None):
		lh_type = self.lhs.analyze(analyzer)
		rh_type = self.rhs.analyze(analyzer)
		self.lineno = lineno
		
		if lh_type is BaseType.STRING:
			raise SemanticError("Strings cannot be used in binary operations",self.lineno)

		if lh_type != rh_type:
			raise SemanticError("Binary operations can only be done with same types",self.lineno)
		else:
			return BaseType.BOOL

class PlusNode(BinopNode):
	
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
		
	def run(self,vm):
		lhs = self.lhs.run(vm)
		rhs = self.rhs.run(vm)

		return lhs - rhs

class TimesNode(BinopNode):
	
	def run(self,vm):
		lhs = self.lhs.run(vm)
		rhs = self.rhs.run(vm)

		return lhs * rhs

class DivideNode(BinopNode):
	def run(self,vm):
		lhs = self.lhs.run(vm)
		rhs = self.rhs.run(vm)

		return lhs / rhs

class EqualsNode(CompareNode):

	def run(self,vm):
		lhs = self.lhs.run(vm)
		rhs = self.rhs.run(vm)

		return lhs == rhs

class NotEqualsNode(CompareNode):
	
	def run(self,vm):
		lhs = self.lhs.run(vm)
		rhs = self.rhs.run(vm)

		return lhs != rhs

class GTNode(CompareNode):
	
	def run(self,vm):
		lhs = self.lhs.run(vm)
		rhs = self.rhs.run(vm)

		return lhs > rhs

class LTNode(CompareNode):

	
	def run(self,vm):
		lhs = self.lhs.run(vm)
		rhs = self.rhs.run(vm)

		return lhs < rhs

class ConstantNode(Node):

	def analyze(self,  analyzer):
		return self.type_name
		
	def __repr__(self):
		return pprint.pformat((self.__class__.__name__,  self.value, self.type_name.name))
	
	def run(self, vm):
		return self.value



class BoolNode(ConstantNode):
	def __init__(self, value, lineno = None):
		self.value = value
		self.type_name = BaseType.BOOL
		self.lineno = lineno

class FloatNode(ConstantNode):
	def __init__(self, value, lineno = None):
		self.value = value
		self.type_name = BaseType.FLOAT
		self.lineno = lineno
class IntNode(ConstantNode):
	def __init__(self, value, lineno = None):
		self.value = value
		self.type_name = BaseType.INT

class StringNode(ConstantNode):
	def __init__(self, value, lineno = None):
		self.value = value
		self.type_name = BaseType.STRING
		self.lineno = lineno
class VarCallNode(Node):
	'''
	Takes a `String` id, and a `BaseType` type.\n
	Checks if variable is declared, and that call is correct.\n
	Returns `type` of var
	
	'''
	def __init__(self,id,call_type, lineno = None):
		self.id = id
		self.call_type = call_type
		self.lineno = lineno
	
	def __repr__(self):
		return pprint.pformat(("VAR_CALL", self.id, self.call_type))
		
	def analyze(self, analyzer, assignment=False, var = None):
		if var is None:
			scope = analyzer.symbol_table_list
		else:
			scope = var["scope"] # revisar el padre 
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
					raise SemanticError("CAN'T CALL UNDEFINDED VAR {0}".format(self.id),self.lineno)
			else:
				var["defined"] = True
				if self.call_type is None:
					return var["type"]
				return self.call_type.analyze(analyzer, var = var, assignment = True)
		else:
			raise SemanticError("CAN'T CALL UNDECLARED VAR {0}".format(self.id),self.lineno)

	def run(self, vm, assignment = False, var = None):
		if var is None:
			scope = [vm.global_symbols]+vm.symbol_scope_list[-1]
		else:
			scope = var["scope"]


		var2 = var
		var = check_if_symbol_declared_scopes(self.id,scope)

		var_space = self.call_type.run(var =var, vm = vm,assignment = assignment)
		#"var[0][1] | var"
		#exec -> ejecuta string como codigo
		#eval -> regresa el valor de la expresion 
		if assignment :
			if var_space is None:
				return None
			exec(var_space + " = assignment")
		else:
			if var_space is None:
				return None
			
			return eval(str(var_space)) 


class SimpleCallNode(Node):
	def __init__(self,dims,lineno=None):
		self.dims = dims
		self.lineno = lineno

	def __repr__(self):
		return pprint.pformat(("Simple Var Call", self.dims ))

	def analyze(self,analyzer : SemanticAnalyzer,var,assignment=False):
		if var["symbol_type"] != "simple":
			raise SemanticError("Expected simple var.\n Recieved: {0}".format(var["symbol_type"]),self.lineno)

		if len(var["dims"]) != len(self.dims):
			return SemanticError("Wrong number of Dimensions! \n Expected: {0}".format(var["dims"]),self.lineno)
		for dim in self.dims:
			dimtype = dim.analyze()

			if dimtype is not BaseType.INT:
				return SemanticError("Index has to be int, found  {0}".format(dimtype),self.lineno)

		return var["type"]

	def run(self, var, vm, assignment = False):
		for (dimcall,dimVar) in zip(self.dims,var["dims"]):
			dimcall = dimcall.run(vm)
			if dimcall >= dimVar:
				raise RuntimeError("Index out of bounds! Max index: {0}, recieved: {1}".format(dimVar,dimcall))
		current_space = "var[\"value\"]"
		for dim in self.dims: # Todo esto por no tener apuntadores :(
			current_space += "[" + dim + "]"
		return current_space

#hDONE
class ReturnNode(Node):
	'''
	Return node analyzes an expresion recieved and executes it\n 
	takes an expresion
	'''
	def __init__(self, expr, lineno = None):
		self.expr = expr
		self.lineno = lineno

	def __repr__(self):
		return pprint.pformat(("RETURN", self.expr))

	def analyze(self, analyzer: SemanticAnalyzer):
		return self.expr.analyze(analyzer)
	
	def run(self,vm):
		return self.expr.run(vm)

class FuncCallNode(Node):
	def __init__(self, callFunc, lineno = None):
		self.callFunc = callFunc
		self.lineno = lineno

	def __repr__(self):
		return pprint.pformat(("FUNC_CALL", self.callFunc))

	def analyze(self, analyzer: SemanticAnalyzer , var = None, assignment=False):
		if var is None:
			scope = analyzer.symbol_table_list
		else:
			scope = var["scope"]
		# revisar que la funcion exista 
		func = check_if_symbol_declared_scopes(self.callFunc["id"],scope)
		if not func:
			raise SemanticError("Function {0} does not exist".format(callFunc["id"]),self.lineno)	
		
		if func["symbol_type"] != "func":
			raise SemanticError("{0} is already declared and is not a func\n".format(func["id"]),self.lineno)

		params = func["params"]

		# checar params que sean de tipo correcto
		if len(func["params"]) != len(self.callFunc["args"]):
			raise SemanticError("Wrong number of arguments in function call {0}".format(func["id"]),self.lineno)
		
		for (index,(param,arg)) in enumerate(zip(func["params"],self.callFunc["args"])):
			param_type = param.dec["type"]
			arg_type = arg.analyze(analyzer)

			if param_type != arg_type:
				raise SemanticError("argument {} is of wrong type.\n Expected {}, recieved {}".format(index,param_type,arg_type),self.lineno)


		# regresar el tipo de regreso
		return func["return_op"]

	def run(self, vm, var = None , assignment = False):

		if var is None:
			scope = [vm.global_symbols]+vm.symbol_scope_list[-1]
		else:
			scope = var["scope"]
		# obtener func de llamada,
		# push nuevo scope
		func = check_if_symbol_declared_scopes(self.callFunc["id"],scope)

		args_result = []
		for arg in self.callFunc["args"]:
			args_result.append(arg.run(vm))

		vm.symbol_scope_list.append([{}])
		#declarar func, para llamada recursiva.
		# declarar_symbol_scopes_run(func,vm.symbol_scope_list,vm.globals)
		# declarar params
		for (index,param) in enumerate(func["params"]):
			param.run(vm)
			param = check_if_symbol_declared_scopes(param.dec["id"],[vm.global_symbols]+vm.symbol_scope_list[-1])
			param["value"] = args_result[index]
		result =func["body"].run(vm)

		vm.symbol_scope_list.pop() 

		return result if var is None else str(result)

		
class ObjectCallNode(Node):
	def __init__(self, dec, lineno = None):
		self.dec = dec
		self.lineno = lineno


	def __repr__(self):
		return pprint.pformat(("VARDEC", self.dec))

	def analyze(self, analyzer: SemanticAnalyzer):
		pass

class ReadNode(Node):
	''' Readnode takes an array of VarCallNodes names as a parameter.\n
		Reads series of inputs into vars, makes them defined.\n
		Returns nothing.\n
		Raises `SemanticError` if var not declared '''
	def __init__(self, variables : [VarCallNode], lineno = None):
		self.variables = variables
		self.lineno = lineno

	def __repr__(self):
		return pprint.pformat(("READ", self.variables))

	def analyze(self, analyzer: SemanticAnalyzer):
		for var in self.variables:
			var = check_if_symbol_declared_scopes(var.id,analyzer.symbol_table_list)
			if not var:
				raise SemanticError("Can't read into variable that's not declared",self.lineno)
			if var["type"] is not BaseType.STRING:
				raise SemanticError("Can only read into String type var",self.lineno)
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
	def __init__(self, expresiones, lineno = None):
		self.expresiones = expresiones 
		self.lineno = lineno

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
	def __init__(self, condition, body, else_body, lineno = None):
		self.condition = condition
		self.body = body
		self.else_body = else_body
		self.lineno = lineno

	def __repr__(self):
		return pprint.pformat(("IfNode", self.condition, self.body, self.else_body))

	def analyze(self, analyzer: SemanticAnalyzer):
		# print("Symbol list:",analyzer.symbol_table_list)
		# Checar que expresion condicion sea bool
		condition_type = self.condition.analyze(analyzer)
		if condition_type is not BaseType.BOOL:
			raise SemanticError("Condition has to return BOOL type",self.lineno)
		
		body_type = self.body.analyze(analyzer)
		
		if self.else_body is None:
			else_body_type = None
		else:
			else_body_type =  self.else_body.analyze(analyzer)

		if body_type != else_body_type:
			raise SemanticError("If body and else body return different types!")
		
		return body_type

	def run(self,vm):
		if self.condition.run(vm) == True:
			return self.body.run(vm)
		else:
			return self.else_body.run(vm)


class WhileNode(Node):
	'''
	Takes a condition and a body.\n 
	evaluates condition and checks if evaluation is `BaseType.BOOL` and if not `raises` `SemanticError`,
	then analyzes `estatutos` in `body`,
	
	'''
	def __init__(self, condition, body, lineno = None):
		self.condition = condition
		self.body = body
		self.lineno = lineno

	def __repr__(self):
		return pprint.pformat(("WHILE", self.condition, self.body))

	def analyze(self, analyzer: SemanticAnalyzer):
		condition_type = self.condition.analyze(analyzer)
		if condition_type is not BaseType.BOOL:
			raise SemanticError("Condition has to return BOOL type",self.lineno)
		self.body.analyze(analyzer)	
	
	def run(self,vm):
		while self.condition.run(vm):
			self.body.run(vm)

class ObjectDecNode(Node):
	'''{"type": p[1], "id": p[2], "defined": False,"symbol_type":"object"}'''
	def __init__(self, dec, lineno = None):
		self.dec = dec
		self.lineno = lineno

	def __repr__(self):
	 return pprint.pformat((self.__class__.__name,self.dec))
	# Analisis semantico : Checar que exita la clase
	def analyze(self,analyzer : SemanticAnalyzer):
		if check_if_symbol_declared_scopes(self.dec["id"],analyzer.symbol_table_list):
			raise SemanticError("Symbol already declared with name {0}".format(self.dec["id"]),self.lineno)
		parent_class = check_if_symbol_declared_scopes(self.dec["type"],analyzer.symbol_table_list)
		if parent_class is False:
			raise SemanticError("Class {0} is not declared".format(parent_class),self.lineno)
		
		if parent_class["symbol_type"] != "class":
			raise SemanticError("{0} is not a class, it's a {1}".format(parent_class["id"],parent_class["symbol_type"]),self.lineno)

		self.dec["scope"] = parent_class["scope"].copy()
		declarar_symbol_scopes(self.dec,analyzer.symbol_table_list)

	# Run: *Copiar* (No referenciar) scope de clase padre

	def run(self,vm):
		scope_padre = check_if_symbol_declared_scopes(self.dec["type"],[vm.global_symbols]+vm.symbol_scope_list[-1])["scope"]
		self.dec["scope"] = scope_padre.copy()
		declarar_symbol_scopes_run(self.dec,vm.symbol_scope_list,vm.global_symbols)

class ForLoopNode(Node):
	'''
	`ForLoopNode` takes a control var, an assignment, a end point, and a body.\n
	Runs body while condition is true.
	'''
	def __init__(self, variable, expresion, end, body, lineno = None):
		self.variable = variable
		self.expresion = expresion
		self.end = end
		self.body = body
		self.lineno = lineno

	def __repr__(self):
		return pprint.pformat(("FOR_LOOP", self.dec))

	def analyze(self, analyzer: SemanticAnalyzer):

		AssignNode(self.variable,self.expresion).analyze(analyzer)

		var_type = check_if_symbol_declared_scopes(self.variable.id,analyzer.symbol_table_list)["type"]
		if var_type is not BaseType.INT:
			raise SemanticError("Can only use ints in for loop",self.lineno)


		end_type = self.end.analyze(analyzer)
		
		if end_type is not BaseType.INT:
			raise SemanticError("Can only use type INT in for loop",self.lineno)
		
		self.body.analyze(analyzer)

	def run(self,vm):
		var = check_if_symbol_declared_scopes(self.variable.id,[vm.global_symbols]+vm.symbol_scope_list[-1])
		var["value"] = self.expresion.run(vm)
		end = self.end.run(vm)
		while var["value"] != end:
			a = self.body.run(vm)
			if a:
				return a
			var["value"] += 1

def generic_error(type,p):
	print("Error in {2}  on line {0} \n At index {1}".format(p.lineno(4), p.lexpos(4),type))

def p_programa(p):
	'''programa : declaraciones main '''
	p[0] = MainNode(p[1], p[2])
	

def p_declaraciones(p):
	'''declaraciones : empty 
					| var_dec SEMICOLON declaraciones
					| funcion_def declaraciones
					| clase_def declaraciones'''
	if len(p) == 2:
		p[0] = []
	elif len(p) == 4:
		p[0] = [p[1]] + p[3] # var dec es de largo diferente
	else:
		p[0] = [p[1]] + p[2]

def p_clase_def(p):
	'''clase_def : CLASS ID clase_op bloque_clase'''
	p[0] = ClassDecNode({"id" : p[2], "inheritance" : p[3], 
		"attributes": p[4]["attributes"], "methods" : p[4]["methods"], "symbol_type":"class"}, lineno = p.lineno(1))


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
	p[0] = FuncDecNode({"id": p[2], "params": p[4], "return_op": p[6],
			"body":p[7], "symbol_type":"func"}, lineno = p.lineno(1))


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
	p[0] = BloqueNode( p[2], lineno = p.lineno(1))


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
		p[0] = ObjectDecNode({"type": p[1], "id": p[2], "defined": True,"symbol_type":"object"}, lineno = p.lineno(2))
	else:
		p[0] = VarDecNode({"type": p[1], "id": p[2], "dims": p[3] , "defined":False, "symbol_type":"simple"}, lineno = p.lineno(2))


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
				| var_dec SEMICOLON
				| expresion SEMICOLON
				| returns SEMICOLON
				| llamada_metodo SEMICOLON
				| lectura SEMICOLON
				| escritura SEMICOLON
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
	p[0] =  AssignNode(p[1], p[3], lineno = p.lineno(2))


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
			p[0]=p[2](p[1], p[3]) 


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
	p[0] = p[1]



def p_var_cte_f(p):
	''' var_cte : CTEF '''
	p[0] = FloatNode(p[1], lineno = p.lineno(1))


def p_var_cte_i(p):
	''' var_cte : CTEI '''
	p[0] = IntNode(p[1], lineno = p.lineno(1))

def p_var_cte_string(p):
	''' var_cte : CTESTRING'''
	p[0] = StringNode(p[1], lineno = p.lineno(1))


def p_var_cte_func_call(p):
	''' var_cte : llamada_funcion '''
	p[0] = p[1]

def p_var_cte_if(p):
	''' var_cte : decision '''
	p[0] = p[1]

def p_var_cte_bloque_func(p):
	''' var_cte : bloque_func '''
	p[0] = p[1]

def p_bool(p):
	''' boolean : TRUE
				| FALSE '''
	p[0] = BoolNode(p[1], lineno = p.lineno(1))

def p_returns(p):
	''' returns : RETURN expresion '''
	p[0] = ReturnNode(p[2], lineno = p.lineno(1))

#! SE QUITO EL SEMICOLON


def p_llamada_funcion(p):
	''' llamada_funcion : ID LPAREN param_llamada RPAREN '''
	p[0] = FuncCallNode({"id": p[1], "args": p[3]}, lineno = p.lineno(1))


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
	p[0] = ReadNode([p[3]]+p[4], lineno = p.lineno(1))


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
	p[0] = VarCallNode( p[1],  p[2], lineno = p.lineno(1))



# Ahorita solo soportamos un nivel de profundidad: a.b, no a.b.c.d()
# no hay method call

'''

DOT varibale variable_op
DIMS 
DOT FUNC_CALL variable_op
empty
'''


def p_variable_op(p):
	''' variable_op : DOT variable
					| LBRACKET expresion RBRACKET 
					| LBRACKET expresion RBRACKET LBRACKET expresion RBRACKET
					| empty
									'''
	if(len(p) == 2):
		p[0] =	SimpleCallNode([], lineno = p.lineno(1))
	elif (len(p) == 3):
		p[0] = p[2]
	elif (len(p) == 4):
		p[0] = SimpleCallNode([p[2]], lineno = p.lineno(1))
	else:
		p[0] = SimpleCallNode([p[2], p[5]], lineno = p.lineno(1))

def p_variable_op_metodo(p):
	''' variable_op : DOT llamada_funcion'''
	p[0] = p[2]


def p_escritura(p):
	''' escritura : WRITE LPAREN expresion op_escritura RPAREN '''
	p[0] = WriteNode([p[3]] + p[4], lineno = p.lineno(1))


def p_op_escritura(p):
	''' op_escritura : COMMA expresion op_escritura
					| empty '''
	if(len(p) == 4):
		p[0] = [p[2]]
	else:
		p[0] = []


def p_decision(p):
	''' decision : IF LPAREN expresion RPAREN bloque_func op_decision '''
	p[0] = IfNode(p[3],p[5], p[6], lineno = p.lineno(1))


def p_op_decision(p):
	''' op_decision : ELSE bloque_func 
					| empty '''
	if(len(p) == 3):
		p[0] = p[2]
	else:
		p[0] = None


def p_repeticion(p):
	''' repeticion : condicional 
					| no_condicional '''
	p[0] = p[1]


def p_condicional(p):
	''' condicional : WHILE LPAREN expresion RPAREN DO bloque_func '''
	p[0] = WhileNode(p[3], p[6], lineno = p.lineno(1))


def p_no_condicional(p):
	''' no_condicional : FROM variable EQUAL expresion TO expresion DO bloque_func '''
	p[0] = ForLoopNode(  p[2], p[4],  p[6], p[8], lineno = p.lineno(1))

def p_empty(p):
	''' empty : '''
	p[0] = None



def p_error(p):
	raise SyntaxError("Syntax error in input!")

precedence = (
	('left', 'PLUS', 'MINUS'),
	('left', 'TIMES', 'DIVIDE'),
)
