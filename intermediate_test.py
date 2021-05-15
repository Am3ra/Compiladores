from parser import *



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

# SemanticAnalyzer(programa_ejemplo).analisis_semantico(None, debug=True)

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
SemanticAnalyzer(programa_ejemplo).analisis_semantico(None, debug=True)
