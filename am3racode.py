from Parser import *
from maquinaVirtual import *
import sys

args = sys.argv
output_filename = "a.out"

if len(args) < 3:
	raise RuntimeError("Expected at least two arguments")

if args[1] != 'build' and args[1] != 'run':
	raise RuntimeError("First argument can only be \'build\' or \'run\'")

if len(args) == 4:
	output_filename = args[3]

if args[1] == 'build':
	with open(args[2], 'r') as file:
		data = file.read()
		a = SemanticAnalyzer(data,debug=False).analisis_semantico(filename = output_filename,debug=True)
else:
	print(VirtualMachine(fileInput=args[2]).run())

