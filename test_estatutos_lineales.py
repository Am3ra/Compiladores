from Parser import *
import pytest as pytest
from maquinaVirtual import VirtualMachine
import itertools


#! ASIGNACION

def test_analisis_semantico_asignacion_variables_inexistentes_error():
	programa_ejemplo = '''
	Main ()
	{
		pedro = 3;
	}
	'''
	with pytest.raises(SemanticError):
		SemanticAnalyzer(programa_ejemplo).analisis_semantico(None)


def test_analisis_semantico_asignacion_variables_existentes():
	programa_ejemplo = '''

	int alan ; 
	float k ;
	string m;

	Main ()
	{
		alan = 3;
	}
	'''
	SemanticAnalyzer(programa_ejemplo).analisis_semantico(None)


def test_analisis_semantico_asignacion_arreglo_existentes():
	programa_ejemplo = '''

	int alan[3] ; 
	float k ;
	string m;

	Main ()
	{
		alan[2] = 3;
	}
	'''
	SemanticAnalyzer(programa_ejemplo).analisis_semantico(None)


def test_analisis_semantico_asignacion_arreglo_dimensiones_erroneas():
	programa_ejemplo = '''

	int alan[3] ; 
	float k ;
	string m;

	Main ()
	{
		alan[2][4] = 3;
	}
	'''
	with pytest.raises(SemanticError):
		SemanticAnalyzer(programa_ejemplo).analisis_semantico(None)

def test_analisis_semantico_asignacion_arreglo_tipo_erroreno():
	programa_ejemplo = '''

	int alan[3] ; 
	float k ;
	string m;

	Main ()
	{
		alan["hola"] = 3;
	}
	'''
	with pytest.raises(SemanticError):
		SemanticAnalyzer(programa_ejemplo).analisis_semantico(None)
def test_analisis_semantico_asignacion_variables_tipo_incorrecto():
	programa_ejemplo = '''

	int alan ; 
	float k ;
	string m;

	Main ()
	{
		alan = false;
	}
	'''
	with pytest.raises(SemanticError):
		SemanticAnalyzer(programa_ejemplo).analisis_semantico(None)

#!BINOP


def test_analisis_semantico_expresion_binop_constantes_iguales():
	programa_ejemplo = '''

	int alan ; 

	Main ()
	{
		alan = 3 + 5;
	}
	'''
	SemanticAnalyzer(programa_ejemplo).analisis_semantico(None)


def test_analisis_semantico_expresion_binop_constantes_tipo_diferentes():
	programa_ejemplo = '''

	int alan ; 

	Main ()
	{
		alan = 3 + false;
	}
	'''
	with pytest.raises(SemanticError):
		SemanticAnalyzer(programa_ejemplo).analisis_semantico(None)


def test_analisis_semantico_expresion_binop_variables_tipos_iguales():
	programa_ejemplo = '''

	int alan ; 
	int f;

	Main ()
	{
		alan = 3;
		f = alan + 1;
	}
	'''
	SemanticAnalyzer(programa_ejemplo).analisis_semantico(None)


binops = ["+", "-", "*", "/", "<", ">", "!=", "=="]


@pytest.mark.parametrize("type, val1 , val2, op", [(x, y, z, w)for x in ["int"] for y in [1, 2] for z in [3, 4] for w in binops])
def test_analisis_semantico_expresiones_iguales_int(type, val1, val2, op):
	programa_ejemplo = '''

	{0} alan ; 
	{0} f;

	Main ()
	{{
		alan = {1};
		f = {2};
		alan {3} f;
	}}
	'''.format(type, val1, val2, op)
	SemanticAnalyzer(programa_ejemplo).analisis_semantico(None)


@pytest.mark.parametrize("type, val1 , val2, op", [(x, y, z, w)for x in ["float"] for y in [11.1, 2.2] for z in [33.0, 4.1] for w in binops])
def test_analisis_semantico_expresiones_iguales_float(type, val1, val2, op):
	programa_ejemplo = '''

	{0} alan ; 
	{0} f;

	Main ()
	{{
		alan = {1};
		f = {2};
		alan {3} f;
	}}
	'''.format(type, val1, val2, op)
	SemanticAnalyzer(programa_ejemplo).analisis_semantico(None)


#! READ


def test_analisis_semantico_read():
	programa_ejemplo = '''

	string alan ; 

	Main ()
	{
		lee(alan);
	}
	'''
	SemanticAnalyzer(programa_ejemplo).analisis_semantico(None)


@pytest.mark.parametrize("type", [(x)for x in ["float", "int", "bool"]])
def test_analisis_semantico_read_type_error(type):
	programa_ejemplo = '''

	{0} alan ; 

	Main ()
	{{
		lee(alan);
	}}
	'''.format(type)
	with pytest.raises(SemanticError):
		SemanticAnalyzer(programa_ejemplo).analisis_semantico(None)


#! FUNC CALL

def test_analisis_semantico_llamada_funcion():
	programa_ejemplo = '''

	Funcion karen() -> int{

		return 3;
	}

	Main ()
	{
		int a;
		a = karen();
	}
	'''  # FUNCIONO!
	SemanticAnalyzer(programa_ejemplo).analisis_semantico(None, debug=False)


def test_analisis_semantico_llamada_func_parametros():
	programa_ejemplo = '''

	Funcion karen(int a, int b, float f) -> int{

		return a;
	}

	Main ()
	{
		int a; 

		a = karen(1,3,3.1);
	}
	'''  # FUNCIONO!
	SemanticAnalyzer(programa_ejemplo).analisis_semantico(None, debug=False)


def test_analisis_semantico_llamada_func_recursiva():
	programa_ejemplo = '''
	
	Funcion karen(int a, int b, float f) -> int{
		a = karen(2,3,4.5);
		return 3;
	}

	Main ()
	{
		int b; 

		b = karen(1,3,3.1);
	}
	'''  # FUNCIONO!
	SemanticAnalyzer(programa_ejemplo).analisis_semantico(None, debug=False)


#! BLOQUE FUNC

def test_analisis_semantico_bloque_func_estatuto():
	programa_ejemplo = '''

	int alan ; 

	Main ()
	{
		{
		
		};
	}
	'''
	SemanticAnalyzer(programa_ejemplo).analisis_semantico(None)


def test_analisis_semantico_bloque_func_estatuto_con_expresiones():
	programa_ejemplo = '''

	int alan ; 

	Main ()
	{
		
		{
			return 3;
		};
		karen = 3;
	}
	'''
	with pytest.raises(SemanticError):
		SemanticAnalyzer(programa_ejemplo).analisis_semantico(None)


def test_analisis_semantico_bloque_func_estatuto_expresion_return():
	programa_ejemplo = '''

	int alan ; 

	Main ()
	{
		alan = 3 + 
			{
				return 5 + if(3<4){
								return 5;
							}else{
								return 6;
							}; 
			};
	}
	'''
	SemanticAnalyzer(programa_ejemplo).analisis_semantico(None)


############################################! VM TESTS ##################################################

#! RETURN
def test_main_return(tmpdir):
	programa_ejemplo = '''
	Main ()
	{
		return 3;
	}
	'''
	d = str(tmpdir / "a.out")
	SemanticAnalyzer(programa_ejemplo).analisis_semantico(filename=d)
	vm = VirtualMachine(fileInput=d)
	assert vm.run() == 3


def test_main_return_none(tmpdir):
	programa_ejemplo = '''
	Main ()
	{
	}
	'''
	d = str(tmpdir / "a.out")
	SemanticAnalyzer(programa_ejemplo).analisis_semantico(filename=d)
	vm = VirtualMachine(fileInput=d)
	assert vm.run() == None


def test_main_return_var(tmpdir):
	programa_ejemplo = '''
	Main ()
	{
		int a;
		a = 3;
		return a;
	}
	'''
	d = str(tmpdir / "a.out")
	SemanticAnalyzer(programa_ejemplo).analisis_semantico(filename=d)
	vm = VirtualMachine(fileInput=d)
	assert vm.run() == 3


#! FUNC CALL
def test_ejecucion_llamada_func_parametros(tmpdir):
	programa_ejemplo = '''

	Funcion karen(int a, int b, float f) -> int{

		return a + b;
	}

	Main ()
	{
		return  karen(1,3,3.1);
	}
	'''  # FUNCIONO!
	d = str(tmpdir / "a.out")
	SemanticAnalyzer(programa_ejemplo).analisis_semantico(filename=d)
	vm = VirtualMachine(fileInput=d)
	assert vm.run() == 4


def test_ejecucion_recursividad():
	programa_ejemplo = '''

	int alan ; 
	Funcion karen(int a) -> int{
		if (a < 3){
			return 1;
		}else{
			return karen(a - 1);
		};
	}

	Main ()
	{
		return karen(3);
	}
	'''
	vm = VirtualMachine()
	parser = yacc.yacc()
	vm.ast = parser.parse(programa_ejemplo)
	assert vm.run() == 1


def test_ejecucion_llamada_pos_matriz(tmpdir):
	programa_ejemplo = '''

	int a [2][3];

	Main ()
	{	
		a[0][1]= 1;
		return a[0][1];
		
	}
	'''  # FUNCIO}
	d = str(tmpdir / "a.out")
	SemanticAnalyzer(programa_ejemplo).analisis_semantico(filename=d)
	vm = VirtualMachine(fileInput=d)
	assert vm.run() == 1

def test_ejecucion_comparacion(tmpdir):
	programa_ejemplo = '''

	Main ()
	{	
		return (-1)<3;
		
	}
	'''  # FUNCIO}
	d = str(tmpdir / "a.out")
	SemanticAnalyzer(programa_ejemplo).analisis_semantico(filename=d,debug=True)
	vm = VirtualMachine(fileInput=d)
	assert vm.run() == True