from Lexer import *

def test_lexer():
	data = " Main si escribe j"
	
	lexer.input(data)
 	
 	
	for tok in lexer:
	    print(tok)