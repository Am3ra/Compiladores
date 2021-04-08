import ply.lex as lex
import ply.yacc as yacc

# Reserved Words
reserved = {
    # 'Programa'  : 'PROGRAM',
    'Clase'     : 'CLASS',
    'hereda'    : 'INHERIT',
    'Funcion'   : 'FUNC',
    # 'void'      : 'VOID',
    'Main'      : 'MAIN',
    'var'       : 'VAR',
    'int'       : 'INT',
    'float'     : 'FLOAT',
    'string'    : 'STRING',
    'returns'   : 'RETURN',
    'lee'       : 'READ',
    'escribe'   : 'WRITE',
    'si'        : 'IF',
    'entonces'  : 'THEN',
    'sino'      : 'ELSE',
    'mientras'  : 'WHILE',
    'hacer'     : 'DO',
    'desde'     : 'FROM',
    'hasta'     : 'TO',
    'hacer'     : 'DO'
}

# Definition of tokens 
tokens = [  'GTHAN', 'LTHAN', 'NOTEQ', 'SAME', 'ID', 'CTEI','CTEF', 'CTESTRING', 'PLUS', 'MINUS', 
            'TIMES', 'DIVIDE', 'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'COMMA', 'SEMICOLON', 'EQUAL', 
            'COLON', 'RET', 'DOT', 'LBRACKET', 'RBRACKET'] + list(reserved.values())

# Regular expressions
t_GTHAN     = r'\>'
t_LTHAN     = r'\<'
t_NOTEQ     = r'!='
t_SAME      = r'=='
t_PLUS      = r'\+'
t_MINUS     = r'-'
t_TIMES     = r'\*'
t_DIVIDE    = r'/'
t_LPAREN    = r'\('
t_RPAREN    = r'\)'
t_LBRACE    = r'\{'
t_RBRACE    = r'\}'
t_COMMA     = r'\,'
t_SEMICOLON = r'\;'
t_EQUAL     = r'\='
t_COLON     = r'\:'
t_RET       = r'->'
t_DOT       = r'\.'
t_LBRACKET  = r'\['
t_RBRACKET  = r'\]'


def t_CTEF(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_CTEI(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_ID(t):
    r'[A-Za-z][A-Za-z0-9]*'
    t.type = reserved.get(t.value, 'ID') #checks for reserved words
    return t

def t_CTESTRING(t):
    r'\"([^\\\n]|(\\.))*?\"'
    return t

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Build the lexer
lexer = lex.lex()

data = " Main si escribe j"

lexer.input(data)


for tok in lexer:
    print(tok)

## FUNCIONA!
def p_programa(p):
	'''programa : definiciones main ''' 

def p_definiciones(p):
	'''definiciones : var_def definiciones
					| funcion_def definiciones
					| clase_def definiciones
					| empty '''
					
def p_clase_def(p):
	'''clase_def : CLASS ID clase_op bloque_clase'''

def p_clase_op(p):
	''' clase_op : INHERIT ID 
				| empty '''

def p_bloque_clase(p):
	''' bloque_clase : LBRACE op_var op_func RBRACE'''


def p_op_func(p):
	''' op_func : funcion_def
				| empty'''

def p_funcion_def(p):
	''' funcion_def : FUNC ID LPAREN params RPAREN return_option bloque_func'''

def p_op_var(p):
	''' op_var : var_def
				| empty'''

def p_return_option(p):
	''' return_option : RET type_simple
					  | empty ''' 


def p_params(p):
	''' params : ID COLON type_simple params_op''' 

def p_params_op(p):
	''' params_op : COMMA params
					| empty ''' 

def p_bloque_func(p):
	''' bloque_func : LBRACE op_var estatutos RBRACE'''

def p_main(p):
	''' main : MAIN  LPAREN RPAREN bloque_func'''
	
def p_var_def(p):
	''' var_def : VAR type_compuesto ID ids SEMICOLON
				| VAR type_simple ID op_vardef SEMICOLON '''

def p_ids(p):
	''' ids : COMMA ID ids
				| empty'''


def p_op_vardef(p):
	''' op_vardef : LBRACKET CTEI RBRACKET 
				  | LBRACKET CTEI RBRACKET LBRACKET CTEI RBRACKET 
				  | empty'''


def p_type_simple(p):
	''' type_simple : INT
					| FLOAT
					| STRING '''

def p_type_compuesto(p):
	''' type_compuesto : ID '''

def p_estatutos(p):
	''' estatutos : estatuto
				| estatuto estatutos
				| empty '''


def p_estatuto(p):
	''' estatuto : asignacion
				| expr
				| returns
				| llamada_void
                | llamada_objeto
				| lectura
				| escritura
				| decision
				| repeticion '''


	
def p_asignacion(p):
	''' asignacion : variable EQUAL expr SEMICOLON '''


def p_expr(p):
	''' expr : expresion
			 | expresion binop expresion '''


def p_expresion(p):
	''' expresion : termino op_expresion '''

def p_op_expresion(p):
    ''' op_expresion : plus_minus expresion 
                     | empty'''

def p_termino(p):
    ''' termino : factor op_factor '''

def p_op_factor(p):
    ''' op_factor : mulop factor
                  | empty '''

def p_factor(p):
    ''' factor : LPAREN expr RPAREN 
               | var_cte
               | variable '''

def p_binop(p):
    ''' binop : SAME
              | NOTEQ
              | GTHAN 
              | LTHAN '''

def p_mulop(p):
    ''' mulop : TIMES 
              | DIVIDE '''

def p_plus_minus(p):
    ''' plus_minus : PLUS
                   | MINUS '''

def p_var_cte(p):
    ''' var_cte : ID
                | CTEF
                | CTEI '''
                
def p_returns(p):
    ''' returns : RETURN expr SEMICOLON '''

def p_llamada_void(p):
    ''' llamada_void : ID LPAREN param_llamada RPAREN SEMICOLON '''

def p_param_llamada(p):
    ''' param_llamada : expr
                      | empty '''

def p_llamada_objeto(p):
    ''' llamada_objeto : ID DOT ID LPAREN param_llamada RPAREN SEMICOLON '''
    
def p_lectura(p):
    ''' lectura : READ LPAREN variable op_lectura RPAREN SEMICOLON '''

def p_op_lectura(p):
    ''' op_lectura : COMMA variable op_lectura 
                   | empty '''

def p_variable(p):
    ''' variable : ID variable_op ''' 
                 

def p_variable_op(p):
	''' variable_op : DOT ID
					| LBRACKET expr RBRACKET matrix
					| empty
					'''

def p_matrix(p):
    ''' matrix : LBRACKET expr RBRACKET matrix
			   | empty ''' 

def p_escritura(p):
    ''' escritura : WRITE LPAREN type_escritura op_escritura RPAREN SEMICOLON '''

def p_type_escritura(p):
    ''' type_escritura : CTESTRING 
                       | expr '''

def p_op_escritura(p):
    ''' op_escritura : COMMA CTESTRING op_escritura 
                     | COMMA expr op_escritura
                     | empty '''
                     
def p_decision(p):
    ''' decision : IF LPAREN expr RPAREN THEN LBRACE estatutos RBRACE op_decision '''

def p_op_decision(p):
    ''' op_decision : ELSE LBRACE estatutos RBRACE 
                    | empty '''

def p_repeticion(p):
    ''' repeticion : condicional 
                   | no_condicional '''

def p_condicional(p):
    ''' condicional : WHILE LPAREN expr RPAREN DO LBRACE estatutos RBRACE '''

def p_no_condicional(p):
    ''' no_condicional : FROM type_no_condicional EQUAL expr TO expr DO LBRACE estatutos RBRACE '''

def p_type_no_condicional(p):
    ''' type_no_condicional : ID
                            | ID LBRACKET expr RBRACKET 
                            | ID LBRACKET expr RBRACKET LBRACKET expr RBRACKET '''  

def p_empty(p):
    ''' empty : '''
    pass  

def p_error(p):
    print("Syntax error in input!")


parser = yacc.yacc()

programa_ejemplo = '''

var int alan ; 

Main ()
{
    lee ( alan.cabello , alan );
    i = 3; 
    hola(i);
    desde i = 1 hasta 10 hacer 
    { 
        escribe("hola", 10);
    }
}
 ''' ## FUNCIONO!


print(parser.parse(programa_ejemplo))
print(parser.parse(programa_ejemplo+";")) ##ERROR