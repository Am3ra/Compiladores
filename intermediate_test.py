from parser import * 
import pytest as pytest


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

SemanticAnalyzer(programa_ejemplo).analisis_semantico(None,debug=True)

