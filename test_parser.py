from parser import * 
import pytest as pytest
import itertools

def test_expresion():
	expr = PlusNode(IntNode(3),IntNode(4))
	analyzer = SemanticAnalyzer(debug=False)
	assert expr.analyze(analyzer) == BaseType.INT

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


def test_analisis_semantico_declaracion_funcion():
	programa_ejemplo = '''

	Funcion alan(){

	}

	Main ()
	{

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

binops = ["+","-","*","/","<",">","!=","=="]
@pytest.mark.parametrize("type, val1 , val2, op",[(x,y,z,w)for x in ["int"] for y in [1,2] for z in [3,4] for w in binops])
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


@pytest.mark.parametrize("type, val1 , val2, op",[(x,y,z,w)for x in ["float"] for y in [11.1,2.2] for z in [33.0,4.1 ] for w in binops])
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


def test_analisis_semantico_read():
	programa_ejemplo = '''

	string alan ; 

	Main ()
	{
		lee(alan);
	}
	'''
	SemanticAnalyzer(programa_ejemplo).analisis_semantico(None)

@pytest.mark.parametrize("type",[(x)for x in ["float", "int", "bool"]])
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


def test_analisis_semantico_if():
	programa_ejemplo = '''

	int alan ; 

	Main ()
	{
		if (true){
			2+3;
		};
	}
	'''
	SemanticAnalyzer(programa_ejemplo).analisis_semantico(None)

def test_analisis_semantico_if_error_condicion():
	programa_ejemplo = '''

	int alan ; 

	Main ()
	{
		if (alan){
			2+3;
		};
	}
	'''
	with pytest.raises(SemanticError):
		SemanticAnalyzer(programa_ejemplo).analisis_semantico(None)

def test_analisis_semantico_if_else():
	programa_ejemplo = '''

	int alan ; 

	Main ()
	{
		if(true)
		{
			alan = 3 * 4; 
		}
		else
		{
			alan = 3 + 3;
		};
	}
	'''
	SemanticAnalyzer(programa_ejemplo).analisis_semantico(None)