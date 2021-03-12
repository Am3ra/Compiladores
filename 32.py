import ply.lex as lex
# List of token names.   This is always required
tokens = (
   'PLUS',
   'MINUS',
   'TIMES',
   'DIVIDE',
   'LPAREN',
   'RPAREN',
   'SCOLON',
   'LBRACKET',
   'RBRACKET',
   'COMMA',
   'COLON',
   'ASSIGN',
   'NE',
   'LT',
   'GT',
   'CTEI',
   'CTEF',
   'ID',
   'CTESTRING'
)

# t_ID        = r'id'
t_SCOLON    = r'\;'
# t_VAR       = r'var'
t_LBRACKET  = r'\{'
t_RBRACKET  = r'\}'
t_COMMA     = r'\,'
t_COLON     = r'\:'
t_ASSIGN    = r'\='
t_PLUS      = r'\+'
t_MINUS     = r'-'
t_TIMES     = r'\*'
t_DIVIDE    = r'/'
t_LPAREN    = r'\('
t_RPAREN    = r'\)'
t_NE        = r'<>'
t_ID        = r'[a-zA-Z]+'
t_CTESTRING = r'\"[a-zA-Z]+\"'
t_LT        = r'\<'
t_GT        = r'\>'
# t_CTEF      = r'\d+.\d*'
# t_CTEI      = r'\d+'
# t_IF        = r'if'
# t_INT       = r'int'
# t_FLOAT     = r'float'

def t_CTEF(t):
    r'\d+.\d*'
    t.value = float(t.value)
    return t


def t_CTEI(t):
    r'\d+'
    t.value = int(t.value)
    return t

# def t_DECIMAL(t):
#     r'\d+\.\d*'
#     t.value = float(t.value)
#     return t


reserved = {
    'if' : 'IF',
    'int' : 'INT',
    'print': 'PRINT',
    'else' : 'ELSE',
    'var' : 'VAR',
    'float' : 'FLOAT',
    'program' : 'PROGRAM',
}

tokens += tuple(reserved.values())

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

def t_reserved(t):
    r'[a-zA-Z][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    return t

t_ignore  = ' \t'
# Build the lexer
lexer = lex.lex()


#########
#TEST
#########

data = '''
3 + 4 * 10 hola
  + -20 *2
  id program int float
  434.23
'''

# Give the lexer some input
lexer.input(data)


for tok in lexer:
    print(tok)



###############
# PARSING


import ply.yacc as yacc

def p_programa(p):
    '''programa : PROGRAM ID SCOLON vars bloque 
                | PROGRAM ID SCOLON bloque'''


def p_vars(p):
    'vars : VAR declaracion'
    # p[0] = p[2]

def p_declaracion(p):
    '''declaracion : nombre COLON tipo SCOLON 
                   | nombre COLON tipo SCOLON declaracion'''

def p_tipo(p):
    '''tipo : INT 
            | FLOAT'''

def p_bloque(p):
    'bloque : LBRACKET estatutos RBRACKET'

def p_estatutos(p):
    '''estatutos : estatuto 
                | estatuto estatutos
    '''

def p_estatuto(p):
    '''estatuto : asignacion 
                   | condicion 
                   | escritura'''

def p_asignacion(p):
    'asignacion : ID ASSIGN expresion SCOLON'

def p_escritura(p):
    'escritura : PRINT LPAREN contenido RPAREN SCOLON'
    print(p[3])

def p_contenido(p):
    '''contenido : CTESTRING 
                | expresion
                | CTESTRING COMMA contenido
                | expresion COMMA contenido '''

def p_expresion(p):
    '''expresion : exp relop exp
                | exp'''

def p_nombre(p):
    '''nombre : ID 
                | ID COMMA nombre'''

def p_condicion(p):
    '''condicion : IF LPAREN expresion RPAREN bloque SCOLON
                    | IF LPAREN expresion RPAREN bloque ELSE bloque SCOLON'''

def p_relop(p):
    ''' relop : LT 
                | GT
                | NE '''

def p_exp(p):
    ''' exp : termino
            | termino addop exp'''

    if p[2] == "+":
        p[0] = p[1] + p[3]
    elif p[2] == "-":
        p[0] = p[1] - [3]

def p_addop(p):
    ''' addop : PLUS 
                | MINUS '''

def p_termino(p):
    ''' termino : factor
                | factor mulop termino'''

def p_mulop(p):
    ''' mulop : TIMES
                | DIVIDE '''

def p_factor(p): 
    ''' factor : LPAREN expresion RPAREN
                | addop varcte'''

def p_varcte(p):
    ''' varcte : ID
                | CTEF
                | CTEI '''

# def 

def p_error(p):
    print("Syntax error in input!")

parser = yacc.yacc()


while True:
   try:
       s = input('''
       program cool {
           print(3-1);
       } ''')
   except EOFError:
       break
   if not s: continue
   result = parser.parse(s)
   print(result)