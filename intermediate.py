from Parser import *
from maquinaVirtual import *


programa_ejemplo = '''

	int cool;
	int vamos;

	Clase team{
		int cool;
		Funcion electron(int a, int b, int c) -> int{
			return 3;
		}
	}

	Main ()
	{
		cool = 3+3;
		int v;
		
	}
	'''  # FUNCIO}

#SemanticAnalyzer(programa_ejemplo).analisis_semantico(None, debug=False)

programa_ejemplo = '''

int alan ; 

Main ()
{
	alan = 9;
	if(alan < 10)
	{
		alan = alan;
	}
	else
	{
		alan = 3;
	};
	return alan;
}
'''
# vm = VirtualMachine()
# parser = yacc.yacc()
# vm.ast = parser.parse(programa_ejemplo)
# print(vm.run())


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

SemanticAnalyzer(programa_ejemplo).analisis_semantico(None,debug=True)