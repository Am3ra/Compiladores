# Compiladores
Clase compiladores ITC

- [Compiladores](#compiladores)
	- [Primera entrega](#primera-entrega)
	- [Segunda Entrega](#segunda-entrega)
	- [Tercera entrega](#tercera-entrega)
	- [Entrega 4](#entrega-4)

## Primera entrega

Lexer y parser terminados en lexerParser.py

Gramatica, Tokens, y Diagrama de Sintaxis se pueden encontrar en [Este Documento de Google docs.](https://docs.google.com/document/d/1ZmIhkVBWFfFo26X79yKM8ew9fTKH6G3cWouWmyAgv64/edit?usp=sharing)

## Segunda Entrega

El parser ahora genera un Arbol de Sintaxis Abstracta (AST) para ayudar en el paso de analisis semantico

Se simplifico y cambio la gramatica

Se separo el lexer, parser, y analizador semantico
Se agrego declaraciones de clases, variables y funciones

Casi se agrega habilidad de llamar funciones


## Tercera entrega

Agregamos capacidad de sistema de tipos
Refactorizamos la funcion Check_if_declaredscope_ para ser más genérica
Modificamos el parser para agregar más funcionalidad al arbol abstracto
Agregamos analisis semantico de:
- Expresion
- operaciones binarias
- valores constantes
- tipos simples

Agregamos nombre defautl al archivo de salida
Agregamos asignacion de variables
Agregamos la funcion de escritura
mejoramos binopNode
agregamos llamadas a variables simples (e.g. a, a[], o a[][])

Se empezo a agregar impresion sobre errores de sintaxis
	- Se creo la funcion generic Error

Agregamos StringNode (agregamos Strings a valores constantes)

Agregamos anotacion de tipo a variables, funciones, y clases para tabla de simbolos

Se cambio el nombre de llamada objeto a llamada metodo

Se agregaron unit tests

 Wrote 60+ tests, finished ReadNode, WriteNode,

IfNode, ForLoopNode.

Added documentation for Declarar Symbol Scopes,  check if declared,
Assign Node, Var Call node
IfNode, WhileNode, ForLoopNode,ReadNode,WriteNode

added stricter type checking to BINOPNode and CompareNode

Changed Parser to use If,while and forloop nodes 

## Entrega 4

Crear VM, y pruebas VM

Agregar soporte de VM para:

- Nodos constantes
- variables simples
- If
- while
- expresiones
	- operaciones binarias
	- operaciones unarias
- returns
- read
- write
- forloop

Agregamos funcionalidad de return al main

agregamos la primer prueba de VM

## Entrega 5:

Ningun avance

## Entrega 6:

- Agregar declaracion de objetos (analisis, y VM)
- Modificar impresion de operaciones
- Agregar interpretacion de variables
- Agregar asignaicon VM variables
- agregar return al main
- agregar soporte para bloque de codigo como estatuto
- agregar pruebas declaracion de objetos
- terminar llamada funcion VM Y SEMANTICO
- agregar pruebas llamadas funcion
- agregar llamadas atributos
- agregar pruebas llamada atributos
- agregar lineas de error a errores semanticosSemanticError


# Entrega 7:

- Agregar pruebas analisis semantico recursividad
- Agregar pruebas analisis semantico while, if y foor loop
- Agregar pruebas ejecución while, if y foor loop
- Pasar if a expresion
- Agregar pruebas de if como expresion
- Agregar bloque func como expresion
- Agregar pruebas analisis semantico if y bloque func como expresion
- Agregar Recursividad VM
- Agregar llamadas a metodos VM
- Agregar herencia analisis semantico