import pytest
from maquinaVirtual import VirtualMachine
from parser import *


def test_main_return():
	programa_ejemplo = '''
	Main ()
	{
		return 3;
	}
	'''  
	vm = VirtualMachine()
	parser = yacc.yacc()
	vm.ast = parser.parse(programa_ejemplo)
	assert vm.run() == 3

def test_main_return_none():
	programa_ejemplo = '''
	Main ()
	{
	}
	'''  
	vm = VirtualMachine()
	parser = yacc.yacc()
	vm.ast = parser.parse(programa_ejemplo)
	assert vm.run() == None

def test_main_return_var():
	programa_ejemplo = '''
	Main ()
	{
		int a;
		a = 3;
		return a;
	}
	'''  
	vm = VirtualMachine()
	parser = yacc.yacc()
	vm.ast = parser.parse(programa_ejemplo)
	assert vm.run() == 3


def test_ejecucion_llamada_func_parametros():
	programa_ejemplo = '''

	Funcion karen(int a, int b, float f) -> int{

		return a + b;
	}

	Main ()
	{
		
		return  karen(1,3,3.1);
	}
	'''  # FUNCIONO!
	vm = VirtualMachine()
	parser = yacc.yacc()
	vm.ast = parser.parse(programa_ejemplo)
	assert vm.run() == 4

# def test_analisis_semantico_llamada_func_parametros_recursivo():
# 	programa_ejemplo = '''

# 	Funcion karen(int a, int b, float f) -> int{

# 		return karen(a,b,f);
# 	}

# 	Main ()
# 	{
		
# 		return  karen(1,3,3.1);
# 	}
# 	'''  # FUNCIONO!
# 	vm = VirtualMachine()
# 	parser = yacc.yacc()
# 	vm.ast = parser.parse(programa_ejemplo)
# 	assert vm.run() == 4

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