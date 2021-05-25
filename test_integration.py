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

def test_ejecucion_assignacion_funcion(tmpdir):
	programa_ejemplo = '''

	Funcion fibonnaci(int n) -> int
	{
		int a;

		a = 0 ;
		return a;
	}

	Main ()
	{
		return fibonnaci(1);
	}
	'''  # FUNCIO
	d = str(tmpdir / "a.out")
	SemanticAnalyzer(programa_ejemplo).analisis_semantico(filename=d)
	vm = VirtualMachine(fileInput=d)
	assert vm.run() == 0

def test_ejecucion_fibonacci_recursivo(tmpdir):
	programa_ejemplo = '''

	Funcion fibonacci(int a) -> int{
		return if (a < 1){
			return 0;
		}else{
			return if (a == 1) {
				return 1;
			}else{
				return (fibonacci(a-1) + fibonacci(a-2));
			};
			
		};
	}

	Main ()
	{
		return fibonacci(6);
	}
	'''  # FUNCIO
	d = str(tmpdir / "a.out")
	SemanticAnalyzer(programa_ejemplo).analisis_semantico(filename=d)
	vm = VirtualMachine(fileInput=d)
	assert vm.run() == 8

def test_ejecucion_factorial_recursivo(tmpdir):
	programa_ejemplo = '''

	Funcion factorial(int n) -> int
	{
		return if(n == 0)
		{
			return 1;
		}
		else
		{
			return (n * factorial( n-1 ) );
		};
	}

	Main ()
	{
		return factorial(4);
	}
	'''  # FUNCIO
	d = str(tmpdir / "a.out")
	SemanticAnalyzer(programa_ejemplo).analisis_semantico(filename=d)
	vm = VirtualMachine(fileInput=d)
	assert vm.run() == 24 


def test_ejecucion_fibonacci(tmpdir):
	programa_ejemplo = '''

	Funcion fibonnaci(int n) -> int
	{
		int a;
		int b;
		int c;
		int i;

		a = 0;
		b = 1;

		return if(n == 0)
		{
			return a;
		}else{

			desde i = 0 hasta n hacer 
			{
				c = a + b;
				a = b;
				b = c;
			};
			
			return b;
		};

	}

	Main ()
	{
		return fibonnaci(4);
	}
	'''  # FUNCIO
	d = str(tmpdir / "a.out")
	SemanticAnalyzer(programa_ejemplo).analisis_semantico(filename=d)
	vm = VirtualMachine(fileInput=d)
	assert vm.run() == 5 


def test_ejecucion_factorial(tmpdir):
	programa_ejemplo = '''

	Funcion factorial(int n) -> int
	{
		int i;
		int f;

		f = 1;

		desde i = 1 hasta n + 1 hacer 
		{
			f = f * i;
		};

		return f;
	}

	Main ()
	{
		return factorial(4);
	}
	'''  # FUNCIO
	d = str(tmpdir / "a.out")
	SemanticAnalyzer(programa_ejemplo).analisis_semantico(filename=d)
	vm = VirtualMachine(fileInput=d)
	assert vm.run() == 24 