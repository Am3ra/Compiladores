from parser import * 
import pytest as pytest


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

SemanticAnalyzer(programa_ejemplo).analisis_semantico(None,debug=True)

