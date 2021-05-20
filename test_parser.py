from Parser import *
import pytest as pytest
import itertools

def test_expresion():
	expr = PlusNode(IntNode(3),IntNode(4))
	analyzer = SemanticAnalyzer(debug=False)
	assert expr.analyze(analyzer) == BaseType.INT
