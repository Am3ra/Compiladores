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