from Parser import *
import pytest as pytest
from maquinaVirtual import VirtualMachine
import itertools

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


############################################! VM TESTS ##################################################

def test_ejecucion_llamada_metodo(tmpdir):
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


	d = str(tmpdir / "a.out")
	SemanticAnalyzer(programa_ejemplo).analisis_semantico(filename=d)
	vm = VirtualMachine(fileInput=d)
	assert vm.run() == 3

def test_ejecucion_llamada_atributo(tmpdir):
	programa_ejemplo = '''

	Clase team{
		int cool;
		Funcion electron() -> int{
			return 3;
		}
	}

	Main ()
	{
		team a;
		a.cool = 3;
		return a.cool;
	}
	'''  # FUNCIO


	d = str(tmpdir / "a.out")
	SemanticAnalyzer(programa_ejemplo).analisis_semantico(filename=d)
	vm = VirtualMachine(fileInput=d)
	assert vm.run() == 3
