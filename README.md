# Compiladores
Clase compiladores ITC

- [Compiladores](#compiladores)
	- [Primera entrega](#primera-entrega)
	- [Segunda Entrega](#segunda-entrega)

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
