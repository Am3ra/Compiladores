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

def test_analisis_semantico_declaracion_variable_en_main():
	programa_ejemplo = '''

	Main ()
	{
		int cool;
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


def test_analisis_declaracion_de_objetos():
	programa_ejemplo = '''

	Clase team{
		int cool;
		Funcion electron(){
			
		}
	}

	Main ()
	{
		team a;
	}
	'''  # FUNCIO

	SemanticAnalyzer(programa_ejemplo).analisis_semantico(None)

def test_analisis_declaracion_de_objetos_llamada_atributo():
	programa_ejemplo = '''

	Clase team{
		int cool;
		Funcion electron(){
			
		}
	}

	Main ()
	{
		team a;
		a.cool = 3;

		return a.cool;
	}
	'''  # FUNCIO

	SemanticAnalyzer(programa_ejemplo).analisis_semantico(None)

def test_analisis_declaracion_de_objetos_llamada_metodo():
	programa_ejemplo = '''

	Clase team{
		Funcion electron() -> int{
			return 3;
		}
	}

	Main ()
	{
		team a;

		return a.electron();
	}
	'''  # FUNCIO

	SemanticAnalyzer(programa_ejemplo).analisis_semantico(None)
	
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


def test_analisis_semantico_llamada_func_parametros():
	programa_ejemplo = '''

	Funcion karen(int a, int b, float f) -> int{

		return 3;
	}

	Main ()
	{
		int a; 

		a = karen(1,3,3.1);
	}
	'''  # FUNCIONO!
	SemanticAnalyzer(programa_ejemplo).analisis_semantico(None,debug=False)

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
	SemanticAnalyzer(programa_ejemplo).analisis_semantico(None,debug=False)


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
	SemanticAnalyzer(programa_ejemplo).analisis_semantico(None,debug=False)


def test_analisis_semantico_while():
	programa_ejemplo = '''

	int alan ; 

	Main ()
	{
		mientras (4 < 10) hacer 
		{
			alan = 3;
		};
	}
	'''
	SemanticAnalyzer(programa_ejemplo).analisis_semantico(None)

def test_analisis_semantico_while_error_condicion():
	programa_ejemplo = '''

	int alan ; 

	Main ()
	{
		mientras (10) hacer 
		{
			alan = 3;
		};
	}
	'''
	with pytest.raises(SemanticError):
		SemanticAnalyzer(programa_ejemplo).analisis_semantico(None)

def test_analisis_semantico_for_loop():
	programa_ejemplo = '''

	int alan ; 

	Main ()
	{
		desde alan = 0 hasta 43 hacer 
		{
			escribe(alan);
		};
	}
	'''
	SemanticAnalyzer(programa_ejemplo).analisis_semantico(None)

def test_analisis_semantico_for_loop_error_condicion():
	programa_ejemplo = '''

	int alan ; 

	Main ()
	{
		desde alan = 0 hasta a>43 hacer  
		{
			escribe(alan);
		};
	}
	'''
	with pytest.raises(SemanticError):
		SemanticAnalyzer(programa_ejemplo).analisis_semantico(None)

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