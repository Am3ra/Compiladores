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

def test_ejecucion_sort_array(tmpdir):
	programa_ejemplo = '''

	int a [4];
	int b [4];
	int temp;
	int i;
	int j;

	Main ()
	{
		a[0] = 4;
		a[1] = 2;
		a[2] = 3;
		a[3] = 1;

		desde i = 0 hasta 4 hacer 
		{
			desde j = 0 hasta 4 hacer 
			{
				temp = 0;
				if(a[j] > a[i])
				{
					temp = a[i];
					a[i] = a[j];
					a[j] = temp;
				};
				
			};
		};

		return a[1];

	}
	'''  # FUNCIO
	d = str(tmpdir / "a.out")
	SemanticAnalyzer(programa_ejemplo).analisis_semantico(filename=d)
	vm = VirtualMachine(fileInput=d)
	assert vm.run() == 2


def test_ejecucion_find_array(tmpdir):
	programa_ejemplo = '''

	int a [4];
	int b [4];
	int temp;
	int i;
	int j;
	int index;
	Main ()
	{
		a[0] = 4;
		a[1] = 2;
		a[2] = 3;
		a[3] = 1;

		desde i = 0 hasta 4 hacer 
		{
			if (a[i] == 3){
				index = i;
			};
		};

		return index;

	}
	'''  # FUNCIO
	d = str(tmpdir / "a.out")
	SemanticAnalyzer(programa_ejemplo).analisis_semantico(filename=d)
	vm = VirtualMachine(fileInput=d)
	assert vm.run() == 2


def test_ejecucion_matrix_multiplication(tmpdir):
	programa_ejemplo = '''

	int a [2][2];
	int b [2][2];	
	int c [2][2];

	Main ()
	{
		int i;
		int j;
		int k;

		desde i = 0 hasta 2 hacer 
		{
			desde j = 0 hasta 2 hacer{
				a[i][j] = i + j;
				b[i][j] = 9 - i - j;
			};
		};
		
		desde i = 0 hasta 2 hacer 
		{
			desde j = 0 hasta 2 hacer
			{
				int temp;
				temp = 0;
				desde k = 0 hasta 2 hacer
				{
					temp = temp + a[i][k] * b[k][j];
				};
				c[i][j] = temp;
			};
		};
	}
	'''  # FUNCIO
	d = str(tmpdir / "a.out")
	SemanticAnalyzer(programa_ejemplo).analisis_semantico(filename=d)
	vm = VirtualMachine(fileInput=d)
	vm.run()

def test_ejecucion_metodos(tmpdir):
	programa_ejemplo = '''
int a[1][2][3];
int f;

Funcion electron() -> int
{
	return 3;
}

Clase alan{
	int promedio;
}

Clase karen hereda alan
{
	int edad;
	int estatura;
	Funcion perro() -> int
	{
		return 7 - 4;
	}
}

Main() 
{
	int b;
	b=5;
	f = 1;
	karen k;
	return k.perro();
}
	'''  # FUNCIO
	d = str(tmpdir / "a.out")
	SemanticAnalyzer(programa_ejemplo).analisis_semantico(filename=d)
	vm = VirtualMachine(fileInput=d)
	assert vm.run() == 3