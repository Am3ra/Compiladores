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


# for tok in lexer:
#     print(tok)

## FUNCIONA!
def p_programa(p):
    '''programa : definiciones main ''' 
    p[0] = ("PROGRAMA", p[1], p[2])

def p_definiciones(p):
    '''definiciones : var_def definiciones
                    | funcion_def definiciones
                    | clase_def definiciones
                    | empty '''
    if (len(p) == 3):
        p[0] = ("DEFINCION", p[1], p[2])
    else:
        p[0] = None

                    
def p_clase_def(p):
    '''clase_def : CLASS ID clase_op bloque_clase'''
    p[0] = ("CLASE_DEF", p[2],p[3],p[4])

def p_clase_op(p):
    ''' clase_op : INHERIT ID 
                | empty '''
    if(len(p) == 2):
        p[0] = ("CLASE_OP", p[2])
    else:
        p[0] = None

def p_bloque_clase(p):
    ''' bloque_clase : LBRACE op_var op_func RBRACE'''
    p[0] = ("BLOQUE_CLASE", p[2],p[3])


def p_op_func(p):
    ''' op_func : funcion_def
                | empty'''
    p[0] = p[1]

def p_funcion_def(p):
    ''' funcion_def : FUNC ID LPAREN params RPAREN return_option bloque_func'''
    p[0] = {"name": p[2], "params": p[4], "return_op":p[5], "body": p[6]}

def p_op_var(p):
    ''' op_var : var_def
                | empty'''
    p[0] = p[1]

def p_return_option(p):
    ''' return_option : RET type_simple
                      | empty ''' 
    if(len(p) == 2):
        p[0] = ("RETURN_OP", p[2])
    else:
        p[0] = None
        
def p_params(p):
    ''' params : ID COLON type_simple params_op'''
    p[0] =  [(p[2] , p[4])] + p[5]

def p_params_op(p):
    ''' params_op : COMMA params
                    | empty ''' 
    if (len(p)== 3):
        p[0] = [p[3]]
    else:
        p[0] = []

def p_bloque_func(p):
    ''' bloque_func : LBRACE op_var estatutos RBRACE'''
    p[0] = ("BLOQUE_FUNC", p[2] , p[3])

def p_main(p):
    ''' main : MAIN LPAREN RPAREN bloque_func'''
    p[0] = ("MAIN", p[4])
    


"""
#! CAMBIO DE GRAMATICA

''' var_def : VAR type_compuesto    ID ids         SEMICOLON
                | VAR type_simple   ID op_var_def  SEMICOLON '''

#! REGLA ELIMINADA                

 ''' ids : COMMA ID ids
                | empty'''

"""

def p_var_def(p):
    ''' var_def : VAR type_compuesto    ID           SEMICOLON
                | VAR type_simple       ID op_vardef  SEMICOLON '''
                # VAR TYPE_COMP VAR1,VAR2... ;
                # VAR TYPE_SIMPLE VAR1;
    if (len(p) == 5):
        p[0] = ("VARDEF",{"type": p[2], "id": p[3] })
    else:
        p[0] = ("VARDEF",{"type": p[2], "id": p[3], "dims" : p[4] })


def p_op_vardef(p):
    ''' op_vardef : LBRACKET CTEI RBRACKET 
                  | LBRACKET CTEI RBRACKET LBRACKET CTEI RBRACKET 
                  | empty'''
    dims = []
    if(len(p) == 4):
        dims =  [p[2]]
    elif (len(p)== 7):
        dims = [p[2],p[5]]
    p[0] = dims

def p_type_simple(p):
    ''' type_simple : INT
                    | FLOAT
                    | STRING '''
    p[0]= p[1]

def p_type_compuesto(p):
    ''' type_compuesto : ID '''
    p[0]= p[1]

def p_estatutos(p):
    ''' estatutos : estatuto
                | estatuto estatutos
                | empty '''
    if(len(p) == 3):
        p[0] = [p[1]]+p[2]
    else:
        p[0] = [p[1]]

def p_estatuto(p):
    ''' estatuto : asignacion
                | expresion
                | returns
                | llamada_funcion
                | llamada_objeto
                | lectura
                | escritura
                | decision
                | repeticion '''
    p[0]= p[1]

    
def p_asignacion(p):
    ''' asignacion : variable EQUAL expresion SEMICOLON '''
    p[0] = ("ASIGN", p[1], p[3])

"""
#! CAMBIO DE GRAMATICA, REGLAS DE EXPRESIONES MODIFICADAS 

''' expr : expresion
             | expresion binop expresion '''

''' expresion : termino op_expresion '''

''' op_expresion : plus_minus expresion 
                     | empty'''
    
''' termino : factor op_factor '''

''' op_factor : mulop factor
                | empty '''

''' factor : LPAREN expr RPAREN 
            | var_cte
            | variable '''
            
''' mulop : TIMES 
              | DIVIDE '''

## ADD ESTO
    expresion : expresion BINOP expresion
               | plus_minus expresion
               | LPAREN expresion RPAREN
               | var_cte     

"""

def p_expresion(p):
    ''' expresion : expresion binop expresion
               | plus_minus expresion
               | LPAREN expresion RPAREN
               | var_cte '''
    if(len(p)==2):
        p[0]=p[1]
    elif(len(p)==3):
        p[0]= ("UNARY_OP",p[1],p[2])
    else:
        print(p[1:])
        p[0]="COOL"


def p_binop(p):
    ''' binop : SAME
              | NOTEQ
              | GTHAN 
              | LTHAN 
              | PLUS
              | MINUS
              | TIMES
              | DIVIDE'''
    p[0] = p[1]


def p_plus_minus(p):
    ''' plus_minus : PLUS
                   | MINUS '''
    p[0] = p [1]

def p_var_cte(p):
    ''' var_cte : variable
                | CTEF
                | CTEI '''

    p[0] = p[1]
                
def p_returns(p):
    ''' returns : RETURN expresion SEMICOLON '''
    p[0] = ("RETURNS", p[2])

def p_llamada_funcion(p):
    ''' llamada_funcion : ID LPAREN param_llamada RPAREN SEMICOLON '''
    p[0] = ("CALL_FUNC",{"name":p[1],"params": p[3]})

"""
#! GRAMATICA CORREGIDA 

''' param_llamada : expresion
                  | empty '''

"""


def p_param_llamada(p):
    ''' param_llamada : expresion
                      | expresion COMMA param_llamada
                      | empty '''
    if(len(p)==2):
        if (p[1] == None):
            p[0] = []
        else:
            p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

def p_llamada_objeto(p):
    ''' llamada_objeto : ID DOT ID LPAREN param_llamada RPAREN SEMICOLON '''
    p[0] = ("CALL_OBJ", {"className": p[1], "methodName": p[3], "params": p[5]})
    
def p_lectura(p):
    ''' lectura : READ LPAREN variable op_lectura RPAREN SEMICOLON '''
    p[0] = ("READ", [p[3]]+p[4])

def p_op_lectura(p):
    ''' op_lectura : COMMA variable op_lectura 
                   | empty '''
    if (len(p)==2):
        p[0]= []
    else:
        p[0] = [p[2]] + p[3]

def p_variable(p):
    ''' variable : ID variable_op ''' 
    p[0] = ("VAR", {"name": p[1], "call_type": p[2]})
                 


#TODO: ADD METHOD CALLS

def p_variable_op(p):
    ''' variable_op : DOT ID
                    | LBRACKET expresion RBRACKET 
                    | LBRACKET expresion RBRACKET LBRACKET expresion RBRACKET
                    | empty
                    '''
    if(len(p) == 2):
        p[0] = ("Simple")
    elif (len(p) == 3):
        p[0] = ("attribute_call", p[2])
    elif (len(p)==4):
        
    elif (len(p) == 4):
        p[0] = ("Array", p[2])
    else:
        p[0] = ("MATRIX", (p[2],p[5]))



"""
#! GRAMATICA MODIFICADA

variable_op : DOT ID
                    | LBRACKET expresion RBRACKET matrix
                    | empty
                    
GRAMATICA ELIMINADA

matrix : LBRACKET expresion RBRACKET
               | empty

"""

def p_escritura(p):
    ''' escritura : WRITE LPAREN type_escritura op_escritura RPAREN SEMICOLON '''
    p[0] = ("WRITE", [p[3]] + p[4])

def p_type_escritura(p):
    ''' type_escritura : CTESTRING 
                       | expresion '''
    p[0] = p[1]

def p_op_escritura(p):
    ''' op_escritura : COMMA CTESTRING op_escritura 
                     | COMMA expresion op_escritura
                     | empty '''
    if(len(p)==4):
        p[0] = [p[2]]
    else:
        p[0] = []

def p_decision(p):
    ''' decision : IF LPAREN expresion RPAREN THEN LBRACE estatutos RBRACE op_decision '''
    p[0] = ("IF_STMT", {"condition": p[3], "estatutos" :p[7], "else": p[9]})

def p_op_decision(p):
    ''' op_decision : ELSE LBRACE estatutos RBRACE 
                    | empty '''
    if(len(p)==4):
        p[0] = [p[3]]
    else:
        p[0] = []

def p_repeticion(p):
    ''' repeticion : condicional 
                   | no_condicional '''
    p[0] = p[1]

def p_condicional(p):
    ''' condicional : WHILE LPAREN expresion RPAREN DO LBRACE estatutos RBRACE '''
    p[0] = ("WHILE", {"condition": p[3], "estatutos" :p[7]})


def p_no_condicional(p):
    ''' no_condicional : FROM variable EQUAL expresion TO expresion DO LBRACE estatutos RBRACE '''
    p[0] = ("FOR", {"VAR":p[2],"ASSIGN": p[4],"END":p[6],"BODY":p[9]})

"""
#! CAMBiO GRAMATICA QUITAR TYPE NO CONDICIONAL

type_no_condicional : ID.ID
                            | ID LBRACKET expresion RBRACKET 
                            | ID LBRACKET expresion RBRACKET LBRACKET expresion RBRACKET

"""
  
def p_empty(p):
    ''' empty : '''
    p[0] = None 

def p_error(p):
    print("Syntax error in input!")

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
)

parser = yacc.yacc()

programa_ejemplo = '''

var int alan ; 

Main ()
{
    lee ( alan.cabello , alan );
    i = 3; 
    hola(i.hola());
    desde i = 1 hasta 10 hacer 
    { 
        escribe("hola", 10);
    }
}
 ''' ## FUNCIONO!


print(parser.parse(programa_ejemplo))
# print(parser.parse(programa_ejemplo+";")) ##ERROR


