from Parser import *
import pytest as pytest
from maquinaVirtual import VirtualMachine
import itertools


#! IF & IF-ELSE
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


#! WHILE

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

#! FOR LOOP

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

############################################! VM TESTS ##################################################

#! WHILE

def test_analisis_while():
	programa_ejemplo = '''

	int alan ; 

	Main ()
	{
		alan = 13;
		mientras (4 < alan) hacer 
		{
			alan = alan - 1;
		};
	}
	'''
	vm = VirtualMachine()
	parser = yacc.yacc()
	vm.ast = parser.parse(programa_ejemplo)
	vm.run()

#! FOR LOOP
def test_ejecucion_for_loop():
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
	vm = VirtualMachine()
	parser = yacc.yacc()
	vm.ast = parser.parse(programa_ejemplo)
	vm.run()


#! IF

def test_ejecucion_if():
	programa_ejemplo = '''

	int alan ; 

	Main ()
	{
		alan = 9;
		if(alan < 10)
		{
			return alan;
		}
		else
		{
			return 3;
		};
	}
	'''
	vm = VirtualMachine()
	parser = yacc.yacc()
	vm.ast = parser.parse(programa_ejemplo)
	assert vm.run() == 9

def test_ejecucion_if_expresion():
	programa_ejemplo = '''

	int alan ; 

	Main ()
	{
		int cool;
		cool = 4;
		alan = if(cool < 10)
			{
				return 3;
			}
			else
			{
				return 5;
			};
		return alan;
	}
	'''
	vm = VirtualMachine()
	parser = yacc.yacc()
	vm.ast = parser.parse(programa_ejemplo)
	assert vm.run() == 3



def test_ejecucion_if_expresion():
	programa_ejemplo = '''

	int alan ; 

	Main ()
	{
		int cool;
		cool = 4;
		alan =3 + if(cool < 10)
			{
				return 3;
			}
			else
			{
				return 5;
			};
		return alan;
	}
	'''
	vm = VirtualMachine()
	parser = yacc.yacc()
	vm.ast = parser.parse(programa_ejemplo)
	assert vm.run() == 6