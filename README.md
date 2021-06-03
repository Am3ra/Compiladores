
# Manual de usuario

## Introducción

**“AM3RACODE”** es un lenguaje orientado a objetos con un leve enfoque a la seguridad de tipos. Para esto, todas las operaciones binarias sólo se pueden hacer entre mismos tipos, y no hay conversión de tipos implícita. Además, se tomó particular cuidado en el análisis de variables, asegurando que una variable está definida antes de su uso, lo cual requirió análisis especial de los estatutos de control (If, for, while, etc.).

## Requerimientos para ejecución
- Para poder hacer uso de este lenguaje se requiere de: 
- Python 3
- Modelo de datos

## Tipos

El lenguaje de programación cuenta con los siguientes tipos de variables disponibles

- Entero - int
- Flotante - float
- Booleano - bool
- Cadena de caracteres - string

También cuenta con funciones las cuales pueden ser de tipo void o del mismo tipo que las variables disponibles. 

## Estructura de un programa

Para la estructura de un programa simple, **“AM3RACODE”** tiene la siguiente estructura

```
<Declaración de variables globales, funciones o clases>
Main()
{
	<Declaración de variables>
	<Estatutos>
}
```

## Declaración de variables

Se puede realizar declaraciones de variables globales, locales (funciones) y de atributos (clases), las cuales se estructuran de la siguiente manera: 

```
<tipo de variable> <id> <dimensiones>;
```
Las *< dimensiones >* se declaran de la siguiente manera [constante entera] y el lenguaje acepta más de 1 dimensión y estas pueden ser omitidas

Ejemplo:
```
int a;
float x;
string s;
bool k;
int z[3][4];
```


## Declaración de funciones

Se puede realizar declaraciones de funciones y de métodos (clases), los cuales se estructuran de la siguiente manera: 

```
Funcion <id> (<parámetros>) -> <tipo retorno>
{
	<Declaración de variables>
	<Estatutos>
}
```
Los *< parámetros >* ,*< Declaración de variables >*, *< tipo retorno >* & *< Estatutos >* puede omitirse en la declaración
Los *< parámetros >* se declaran de la misma manera que las variables no dimensionadas

Ejemplo:

```
Funcion hola()
{

}

Funcion adios() -> int
{
	int a; //Variable de tipo entero
	a = 3; //Asignación a variable
	return a; //Retorno del mismo tipo
}
```

## Declaración de clases

Se pueden realizar declaraciones de clases, que pueden incluir métodos y atributos, así como herencia.

```
Clase <id> hereda <nombre>
{
	<Declaración de atributos>
	<Declaración de métodos>
	<Estatutos>
}
```
*hereda < nombre >* ,*< Declaración de atributos >*, *< Declaración de métodos >* & *< Estatutos >* puede omitirse en la declaración

Ejemplo:

```
Clase hola
{

}

Clase adios hereda hola
{
	int a;
	int b;
	Funcion perro()
	{

	}
}
```


## Estatutos disponibles

El lenguaje **“AM3RACODE”** contiene los siguientes estatutos

### Asignación

La asignación del lenguaje puede efectuarse con constantes o con expresiones y funciona de la siguiente manera:

```
<variable> = <expresión>;
```
Las **< variables >** pueden ser objetos, variables simples o variables dimensionadas

Ejemplo:
```
int a;
a = 3 + 6;
Clase hola
{
	int c;
}

Main()
{
	hola a;
	a.c = 4;
}
```

```
int a[4];
a[0] = 3;
```

### Declaración de variables

La declaración de variables en estatutos funciona de la misma manera que las globales, solo que estas tienen un alcance local.
  
### Declaración de objetos

La declaración de objetos se realiza de la siguiente manera
```
<id clase> <id>;
```

Ejemplo:
```
Clase hola
{
	int c;
}

Main()
{
	hola a;
}
```

### Expresiones

Dentro de las expresiones podemos ejecutar tanto expresiones algebraicas como bloques de código.

Ejemplo:
```
int a;

Main()
{
	a = 3 + if (3<6){return 5;}else{return 6;};
}
```


*El lenguaje puede utilizar los siguientes operadores:*

- Aritméticos: +, -, *, /
- Comparación: ==, !=, >, <
- Paréntesis, los cuales ayudan a la precedencia en la ejecución de expresion 

### Return
Return saca el resultado de una expresión de su alcance léxico al alcance léxico padre. A diferencia de otros lenguajes, no termina la ejecución de la función ni hace que la función regrese el valor a menos de que el return se encuentre en el alcance más externo.

```
return <expresión>;
```

Ejemplo:

```
int a;
a = 3;
return a;
```

### Llamadas a métodos

Las llamadas a métodos utilizan la declaración de objetos para utilizar los métodos del objeto, funcionan de la siguiente manera:

```
<id> . <id>( < parametros > );
```

Donde *< parametros >* puede omitirse

Ejemplo:

```
Clase perro
{
	Funcion cool(int a) -> int
	{
		return a+3;
	}
}

Main()
{
	perro a; 
	return a.cool(3);
}
```

### Llamadas a funciones
Las llamadas a funciones funcionan de la siguiente manera:
```
<id>( < parametros > );
```
Donde *< parametros >* puede omitirse

Ejemplo:
```
Funcion cool(int a) -> int
{
   return a+3;
}

Main()
{
	return cool(3);
}
```


### Lectura

El estatuto de lectura solo acepta lectura a una o más variables de tipo String, y funciona de la siguiente manera:

```
lee ( <variables> ) ;
```

Ejemplo:

```
string alan ;

Main ()
{
	lee(alan);
	return alan;
}
```


### Escritura

El estatuto de escritura requiere una o más expresiones para escribir en consola, y funciona de la siguiente manera:

```
escribe( <expresiones> );
```

Ejemplo:

```
int alan ;

    Main ()
    {
        alan = 3;
        escribe(alan);    
    }
```

### Repetición     

#### While
El estatuto while está estructurado de la siguiente manera, y se utiliza para correr estatutos hasta que la condición establecida sea falsa
```
mientras ( <condición> ) hacer 
{
<estatutos>
};
```
Donde *< estatutos >* puede omitirse

Ejemplo:

```
int alan ;

Main ()
{
	mientras (4 < 10) hacer
	{
		alan = 3;
	};
}
```


#### Do While

El estatuto Do while funciona de la misma manera que el estatuto While, solo que su estructura está establecida de la siguiente manera:

```
hacer 
{
	<estatutos>
} mientras ( < condición > );
```
Donde *< estatutos >* puede omitirse

Ejemplo:
```		
hacer
{
   alan = 3;
}
mientras (p < 10);
```


#### For
El estatuto For funciona hasta que la expresión brindada cumpla con la condición establecida, y está estructurado de la siguiente manera:

```
desde <id> = <expresión> hasta <int> hacer 
{
	<estatutos>
};
```
Donde *< estatutos >* puede omitirse

Ejemplo:

```
desde alan = 0 hasta 43 hacer  
{
    escribe(alan);
};
```

### Decisión    

#### If
El estatuto if sirve como decisión, si es que la condición del if no se cumple se ejecuta el cuerpo del else, y está estructurado de la siguiente manera:

```
if ( < condición > ) 
{
	<estatutos>
}
else 
{
	<estatutos>
};
```
Donde *< estatutos >* puede omitirse

Ejemplo:
```
if(true)
        {
            alan = 3 * 4;
        }
        else
        {
            alan = 3 + 3;
        };
```

*Si en los estatutos del if, se encuentra el estatuto return, se debe agregar el return en el else y estos 2 deben ser del mismo tipo.* 


## Cómo ejecutar un archivo de texto:
Para usar el compilador, es necesario correr el programa con la siguiente sintaxis: 

python3 am3racode.py build  *< archivo de entrada >* *< archivo de salida >*

Si no se incluye el archivo de salida como parámetro, el valor predeterminado es “a.out”. Esto compila el archivo de entrada, y genera un ejecutable.

Para ejecutar el ejecutable, es necesario correr:

python3 am3racode.py run *< archivo de entrada >*

Si el main() regresa un valor, este se imprime en consola

## Ejemplos

```
Función hola(int n) -> int
{
	int a;
	a = 0 ;
	return a;
}
Main ()
{
	return hola(1);
}
```

```
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
```
