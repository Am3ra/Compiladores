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

def test_analisis_semantico_declaracion_clase_con_herencia():
	programa_ejemplo = '''

	Clase hola
	{
		int p;
		Funcion adios()->int
		{
			return 3;
		}
	}

	Clase team hereda hola{
		int cool;
		Funcion electron(){
			
		}
	}

	Main ()
	{	
		team karalan;

		return karalan.adios();
		
	}
	'''  # FUNCIO}
	vm = VirtualMachine()
	parser = yacc.yacc()
	vm.ast = parser.parse(programa_ejemplo)
	assert vm.run() == 3

