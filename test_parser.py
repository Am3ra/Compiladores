from parser import * 
import pytest as pytest

def test_expresion():
	expr = PlusNode(IntNode(3),IntNode(4))
	analyzer = SemanticAnalyzer("",debug=True)
	assert expr.analyze(analyzer) == BaseType.INT

def test_analisis_semantico():
	programa_ejemplo = '''

	int alan ; 
	float k ;

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
		alan = 3;
		alan + k;
		lee ( alan.cabello , alan );
		i = 3*3-1/-(alan+b); 
		hola(i.hola);
		desde i = 1 hasta 10 hacer 
		{ 
			escribe("hola", 10);
		}
	}
	'''  # FUNCIONO!


    # print(parser.parse(programa_ejemplo+";")) ##ERROR
	SemanticAnalyzer(programa_ejemplo).analisis_semantico(None,debug=True)


def test_analisis_semantico_declaracion_variables():
	programa_ejemplo = '''

	int alan ; 
	float k ;
	string m;

	Main ()
	{

	}
	''' 



	SemanticAnalyzer(programa_ejemplo).analisis_semantico(None,debug=True)

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
