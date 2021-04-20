import ply.lex as lex

# Reserved Words
reserved = {
    # 'Programa'  : 'PROGRAM',
    'Clase': 'CLASS',
    'hereda': 'INHERIT',
    'Funcion': 'FUNC',
    # 'void'      : 'VOID',
    'Main': 'MAIN',
    'var': 'VAR',
    'int': 'INT',
    'float': 'FLOAT',
    'string': 'STRING',
    'returns': 'RETURN',
    'lee': 'READ',
    'escribe': 'WRITE',
    'si': 'IF',
    'entonces': 'THEN',
    'sino': 'ELSE',
    'mientras': 'WHILE',
    'hacer': 'DO',
    'desde': 'FROM',
    'hasta': 'TO',
    'hacer': 'DO',
	'bool': "BOOL"
}

# Definition of tokens
tokens = ['GTHAN', 'LTHAN', 'NOTEQ', 'SAME', 'ID', 'CTEI', 'CTEF', 'CTESTRING', 'PLUS', 'MINUS',
          'TIMES', 'DIVIDE', 'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'COMMA', 'SEMICOLON', 'EQUAL',
          'COLON', 'RET', 'DOT', 'LBRACKET', 'RBRACKET', 'TRUE', 'FALSE'] + list(reserved.values())

# Regular expressions
t_GTHAN = r'\>'
t_LTHAN = r'\<'
t_NOTEQ = r'!='
t_SAME = r'=='
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_COMMA = r'\,'
t_SEMICOLON = r'\;'
t_EQUAL = r'\='
t_COLON = r'\:'
t_RET = r'->'
t_DOT = r'\.'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'


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
    t.type = reserved.get(t.value, 'ID')  # checks for reserved words
    return t


def t_CTESTRING(t):
    r'\"([^\\\n]|(\\.))*?\"'
    return t

def t_TRUE(t):
    r'(true)'
    t.value = True
    return t

def t_FALSE(t):
    r'(false)'
    t.value = False
    return t


# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Error handling rule


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Build the lexer
lexer = lex.lex()

