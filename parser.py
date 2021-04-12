import ply.yacc as yacc
from lexer import lexer
from lexer import tokens
# from semanticAnalyzer import SemanticAnalyzer

class SemanticAnalyzer():
    def __init__(self,input):
        self.input = input
        self.main : MainNode = parser.parse(input)
        self.symbol_table_vars_list = [{}]
        self.symbol_table_funcs_list = [{}]

    def analisis_semantico(self):
        self.main.analyze(self)

    def check_if_declared(self,dec,typeDec):
        for function in self.symbol_table_funcs_list:
            if(function.get(dec["id"]) is not None):
                raise SyntaxError("{0} YA DECLARADA COMO FUNCION:".format(typeDec) + dec["id"])
        
        for var in self.symbol_table_vars_list:
            if(var.get(dec["id"]) is not None):
                raise SyntaxError("{0} YA DECLARADA COMO VARIABLE:".format(typeDec) + dec["id"])

    def declarar_var(self,dec):
        ##Ya se declaro?
        self.check_if_declared(dec,"VARIABLE")
        self.symbol_table_vars_list[-1][dec.id] = dec

    
    def declarar_func(self,dec):
        self.check_if_declared(dec,"FUNCION")
        self.symbol_table_funcs_list[-1][dec.id] = dec



# SemanticAnalyzer(text).analisis_semantico()

class Node():
    def analyze(self, analyzer : SemanticAnalyzer):
        '''Complete Semantic analysis of this node ''' 
        pass

class MainNode(Node):
    def __init__(self, declaraciones , main ):
        self.declaraciones = declaraciones
        self.main = main
    

    def analyze(self, analyzer : SemanticAnalyzer):
        ## Analyzar declaraciones

        ## Analyzar el main

        ##
        for dec in self.declaraciones:
            dec.analyze()
        
        self.main.analyze()
    
    def __str__(self):
        return "{0}".format(("Programa" , self.declaraciones, self.main))

class VarDecNode(Node):
    def __init__(self):
        super().__init__()
    
    def __str__(self):
        return super().__str__()
    
    def analyze(self, analyzer):
        return super().analyze(analyzer)

# FUNCIONA!
def p_programa(p):
    '''programa : declaraciones main '''
    p[0] = MainNode(p[1],p[2])


def p_declaraciones(p):
    '''declaraciones : var_def declaraciones
                    | funcion_def declaraciones
                    | clase_def declaraciones
                    | empty '''
    if (len(p) == 3):
        p[0] = [p[1]] + p[2]
    else:
        p[0] = []


def p_clase_def(p):
    '''clase_def : CLASS ID clase_op bloque_clase'''
    p[0] = ("CLASE_DEF", p[2], p[3], p[4])


def p_clase_op(p):
    ''' clase_op : INHERIT ID 
                | empty '''
    if(len(p) == 2):
        p[0] = ("CLASE_OP", p[2])
    else:
        p[0] = None


def p_bloque_clase(p):
    ''' bloque_clase : LBRACE op_var op_func RBRACE'''
    p[0] = ("BLOQUE_CLASE", p[2], p[3])


def p_op_func(p):
    ''' op_func : funcion_def
                | empty'''
    p[0] = p[1]


def p_funcion_def(p):
    ''' funcion_def : FUNC ID LPAREN params RPAREN return_option bloque_func'''
    p[0] = {"name": p[2], "params": p[4], "return_op": p[6], "vars" : p[7]["VARS"], "estatutos":p[7]["Estatutos"] }


def p_op_var(p):
    ''' op_var : var_def
                | empty'''
    p[0] = p[1]


def p_return_option(p):
    ''' return_option : RET type_simple
                      | empty '''
    if(len(p) == 3):
        p[0] =  p[2]
    else:
        p[0] = None

#! PARAMS AHORA PUEDE SER EMPTY

def p_params(p):
    ''' params : ID COLON type_simple params_op
               | empty'''
    if(len(p) == 5):
        p[0] = [(p[2], p[4])] + p[5]
    else:
        p[0] = []

def p_params_op(p):
    ''' params_op : COMMA params
                    | empty '''
    if (len(p) == 3):
        p[0] = [p[3]]
    else:
        p[0] = []


def p_bloque_func(p):
    ''' bloque_func : LBRACE op_var estatutos RBRACE'''
    p[0] = {"VARS" : p[2], "Estatutos" : p[3] }


def p_main(p):
    ''' main : MAIN LPAREN RPAREN bloque_func'''
    p[0] =  p[4]


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
        p[0] = ("VARDEF", {"type": p[2], "id": p[3]})
    else:
        p[0] = ("VARDEF", {"type": p[2], "id": p[3], "dims": p[4]})


def p_op_vardef(p):
    ''' op_vardef : LBRACKET CTEI RBRACKET 
                  | LBRACKET CTEI RBRACKET LBRACKET CTEI RBRACKET 
                  | empty'''
    dims = []
    if(len(p) == 4):
        dims = [p[2]]
    elif (len(p) == 7):
        dims = [p[2], p[5]]
    p[0] = dims


def p_type_simple(p):
    ''' type_simple : INT
                    | FLOAT
                    | STRING '''
    p[0] = p[1]


def p_type_compuesto(p):
    ''' type_compuesto : ID '''
    p[0] = p[1]


def p_estatutos(p):
    ''' estatutos : estatuto
                | estatuto estatutos
                | empty '''
    if(len(p) == 3):
        p[0] = [p[1]]+p[2]
    else:
        if p[1] == None:
            p[0] = []
        else:
            p[0] = [p[1]]

#! SE AGREGO SEMICOLON A LLAMADA_FUNC Y LLAMADA_OBJ


def p_estatuto(p):
    ''' estatuto : asignacion
                | expresion
                | returns
                | llamada_funcion SEMICOLON
                | llamada_objeto SEMICOLON
                | lectura
                | escritura
                | decision
                | repeticion '''
    p[0] = p[1]


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
    if(len(p) == 2):
        p[0] = p[1]
    elif(len(p) == 3):
        p[0] = ("UNARY_OP", p[1], p[2])
    else:
        print(p[1:])
        p[0] = "COOL"


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
    p[0] = p[1]


def p_var_cte(p):
    ''' var_cte : variable
                | CTEF
                | CTEI '''

    p[0] = p[1]


def p_returns(p):
    ''' returns : RETURN expresion SEMICOLON '''
    p[0] = ("RETURNS", p[2])

#! SE QUITO EL SEMICOLON


def p_llamada_funcion(p):
    ''' llamada_funcion : ID LPAREN param_llamada RPAREN '''
    p[0] = ("CALL_FUNC", {"name": p[1], "params": p[3]})


"""
#! GRAMATICA CORREGIDA 

''' param_llamada : expresion
                  | empty '''

"""


def p_param_llamada(p):
    ''' param_llamada : expresion
                      | expresion COMMA param_llamada
                      | empty '''
    if(len(p) == 2):
        if (p[1] == None):
            p[0] = []
        else:
            p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]


def p_llamada_objeto(p):
    ''' llamada_objeto : ID DOT ID LPAREN param_llamada RPAREN  '''
    p[0] = ("CALL_OBJ", {"className": p[1],
            "methodName": p[3], "params": p[5]})


def p_lectura(p):
    ''' lectura : READ LPAREN variable op_lectura RPAREN SEMICOLON '''
    p[0] = ("READ", [p[3]]+p[4])


def p_op_lectura(p):
    ''' op_lectura : COMMA variable op_lectura 
                   | empty '''
    if (len(p) == 2):
        p[0] = []
    else:
        p[0] = [p[2]] + p[3]

#! SE AGREGO LLAMADA OBJETO


def p_variable(p):
    ''' variable : ID variable_op
                  | llamada_objeto '''
    if(len(p) == 3):
        p[0] = ("VAR", {"name": p[1], "call_type": p[2]})
    else:
        p[0] = p[1]


def p_variable_op(p):
    ''' variable_op : DOT ID 
                    | LBRACKET expresion RBRACKET 
                    | LBRACKET expresion RBRACKET LBRACKET expresion RBRACKET
                    | empty
                    '''
    if(len(p) == 2):
        if(p[1] == None):
            p[0] = ("Simple")
        else:
            p[0] = ("method_call", p[1])
    elif (len(p) == 3):
        p[0] = ("attribute_call", p[2])
    elif (len(p) == 4):
        p[0] = ("Array", p[2])
    else:
        p[0] = ("MATRIX", (p[2], p[5]))


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
    if(len(p) == 4):
        p[0] = [p[2]]
    else:
        p[0] = []


def p_decision(p):
    ''' decision : IF LPAREN expresion RPAREN THEN LBRACE estatutos RBRACE op_decision '''
    p[0] = ("IF_STMT", {"condition": p[3], "estatutos": p[7], "else": p[9]})


def p_op_decision(p):
    ''' op_decision : ELSE LBRACE estatutos RBRACE 
                    | empty '''
    if(len(p) == 4):
        p[0] = [p[3]]
    else:
        p[0] = []


def p_repeticion(p):
    ''' repeticion : condicional 
                   | no_condicional '''
    p[0] = p[1]


def p_condicional(p):
    ''' condicional : WHILE LPAREN expresion RPAREN DO LBRACE estatutos RBRACE '''
    p[0] = ("WHILE", {"condition": p[3], "estatutos": p[7]})


def p_no_condicional(p):
    ''' no_condicional : FROM variable EQUAL expresion TO expresion DO LBRACE estatutos RBRACE '''
    p[0] = ("FOR", {"VAR": p[2], "ASSIGN": p[4], "END": p[6], "BODY": p[9]})


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

Funcion karen() -> int 
{
    
}

Main ()
{
    lee ( alan.cabello , alan );
    i = 3; 
    hola(i.hola);
    desde i = 1 hasta 10 hacer 
    { 
        escribe("hola", 10);
    }
}
 '''  # FUNCIONO!


print(parser.parse(programa_ejemplo))
# print(parser.parse(programa_ejemplo+";")) ##ERROR




