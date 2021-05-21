from Parser import *
from maquinaVirtual import *


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

