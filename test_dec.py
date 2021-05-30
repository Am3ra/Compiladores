from Parser import *
import pytest as pytest
from maquinaVirtual import VirtualMachine
import itertools


#! Clases

def test_analisis_semantico_declaracion_clase_con_variable_global():
	programa_ejemplo = '''

	int cool;

	Clase team{
		int cool;
		Funcion electron(){
			
		}
	}

	Main ()
	{
		
	}
	'''  # FUNCIO}

	SemanticAnalyzer(programa_ejemplo).analisis_semantico(None,debug=False)

def test_analisis_semantico_declaracion_clase_con_herencia():
	programa_ejemplo = '''

	Clase hola
	{
		int p;
		Funcion adios()
		{

		}
	}

	Clase team hereda hola{
		int cool;
		Funcion electron(){
			
		}
	}

	Main ()
	{
		
	}
	'''  # FUNCIO}

	SemanticAnalyzer(programa_ejemplo).analisis_semantico(None,debug=False)

def test_analisis_semantico_declaracion_clase_error_atributos_dobles():
	programa_ejemplo = '''

	Clase team{
		int cool;
		int cool;
		Funcion electron(){
			
		}
	}

	Main ()
	{

	}
	'''  # FUNCIO

	with pytest.raises(SemanticError):
		SemanticAnalyzer(programa_ejemplo).analisis_semantico(None,debug=False)


def test_analisis_semantico_declaracion_clase_doble_error():
	programa_ejemplo = '''

	Clase team{

	}

	Clase team{
		
	}

	Main ()
	{

	}
	'''  # FUNCIO

	with pytest.raises(SemanticError):
		SemanticAnalyzer(programa_ejemplo).analisis_semantico(None,debug=False)

def test_analisis_semantico_declaracion_clase_error_metodos_dobles():
	programa_ejemplo = '''

	Clase team{
		int cool;
		Funcion electron(){
			
		}
		Funcion electron(){
			
		}
	}

	Main ()
	{

	}
	'''  # FUNCIO

	with pytest.raises(SemanticError):
		SemanticAnalyzer(programa_ejemplo).analisis_semantico(None,debug=False)


#! Funciones

def test_analisis_semantico_declaracion_funcion():
	programa_ejemplo = '''

	Funcion alan(){

	}

	Main ()
	{
		int cool;
	}
	'''  # FUNCIONO!

	SemanticAnalyzer(programa_ejemplo).analisis_semantico(None,debug=False)


def test_analisis_semantico_declaracion_funcion_returns():
	programa_ejemplo = '''

	Funcion karen() -> int{

		return 3;
	}

	Main ()
	{

	}
	'''  # FUNCIONO!
	SemanticAnalyzer(programa_ejemplo).analisis_semantico(None,debug=False)


def test_analisis_semantico_declaracion_funcion_returns_error():
	programa_ejemplo = '''

	Funcion karen() -> int{

	}

	Main ()
	{

	}
	'''  # FUNCIONO!
	with pytest.raises(SemanticError):
		SemanticAnalyzer(programa_ejemplo).analisis_semantico(None,debug=False)


def test_analisis_semantico_declaracion_funcion_returns_wrong_type_error():
	programa_ejemplo = '''

	Funcion karen() -> int{

		return 3.2;
	}

	Main ()
	{

	}
	'''  # FUNCIONO!
	with pytest.raises(SemanticError):
		SemanticAnalyzer(programa_ejemplo).analisis_semantico(None,debug=False)


def test_analisis_semantico_declaracion_funcion_error():
	programa_ejemplo = '''

	Funcion alan(){

	}

	Funcion alan() -> int {

	}

	Main ()
	{

	}
	'''  # FUNCIONO!

	with pytest.raises(SemanticError):
		SemanticAnalyzer(programa_ejemplo).analisis_semantico(None,debug=False)


def test_analisis_semantico_declaracion_funcion_error_syntaxis():
	programa_ejemplo = '''

	Funcion alan() -> int , int{

	}



	Main ()
	{

	}
	'''  # FUNCIONO!

	with pytest.raises(SyntaxError):
		SemanticAnalyzer(programa_ejemplo).analisis_semantico(None,debug=False)

def test_analisis_semantico_dec_func_parametros():
	programa_ejemplo = '''

	Funcion karen(int a, int b, float f) -> int{

		return 3;
	}

	Main ()
	{

	}
	'''  # FUNCIONO!
	SemanticAnalyzer(programa_ejemplo).analisis_semantico(None,debug=False)

#! VARIABLES


def test_analisis_semantico_declaracion_variables():
	programa_ejemplo = '''

	int alan ; 
	float k ;
	string m;

	Main ()
	{

	}
	''' 



	SemanticAnalyzer(programa_ejemplo).analisis_semantico(None,debug=False)


def test_analisis_semantico_declaracion_arreglos():
	programa_ejemplo = '''

	int alan [3]; 
	float k ;
	string m;

	Main ()
	{

	}
	''' 

	SemanticAnalyzer(programa_ejemplo).analisis_semantico(None,debug=False)


def test_analisis_semantico_declaracion_matrices():
	programa_ejemplo = '''

	int alan [3][6]; 
	float k ;
	string m;

	Main ()
	{

	}
	''' 

	SemanticAnalyzer(programa_ejemplo).analisis_semantico(None,debug=False)

def test_analisis_semantico_declaracion_cubos():
	programa_ejemplo = '''

	int alan [3][6][9]; 
	float k ;
	string m;

	Main ()
	{

	}
	''' 

	SemanticAnalyzer(programa_ejemplo).analisis_semantico(None,debug=False)


def test_analisis_semantico_declaracion_variables_error():
	programa_ejemplo = '''

	int alan b; 
	float k ;
	string m;

	Main ()
	{

	}
	'''
	with pytest.raises(SyntaxError): 
		SemanticAnalyzer(programa_ejemplo).analisis_semantico(None)

def test_analisis_semantico_declaracion_variable_en_main():
	programa_ejemplo = '''

	Main ()
	{
		int cool;
	}
	'''  # FUNCIO}

	SemanticAnalyzer(programa_ejemplo).analisis_semantico(None,debug=False)

############################################! VM TESTS ##################################################

#! CLASE

def test_ejecucion_declaracion_matriz(tmpdir):
	programa_ejemplo = '''

	int a [2][3];

	Main ()
	{	
			
		
	}
	'''  # FUNCIO}
	d = str(tmpdir / "a.out")
	SemanticAnalyzer(programa_ejemplo).analisis_semantico(filename=d)
	vm = VirtualMachine(fileInput=d)
	vm.run()

def test_ejecucion_declaracion_alcances_error(tmpdir):
	programa_ejemplo = '''

	int a ;

	Main ()
	{	
		{
			int a;
		};
		a = 4;
	}
	'''  # FUNCIO}
	d = str(tmpdir / "a.out")
	with pytest.raises(SemanticError):
		SemanticAnalyzer(programa_ejemplo).analisis_semantico(filename=d)
		vm = VirtualMachine(fileInput=d)
		vm.run()
		
