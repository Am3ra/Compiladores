import pytest
from maquinaVirtual import VirtualMachine
from Parser import *


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
