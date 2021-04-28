import pytest
from maquinaVirtual import VirtualMachine
from parser import *


def test_director(tmpdir):
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
	'''  
	vm = VirtualMachine()
	parser = yacc.yacc()
	vm.ast = parser.parse(input)
	vm.run()