from parser import *
import pickle


class VirtualMachine():
	'''
	This class takes a file path, reads the file, and executes it.\n
	Runs the recursive descent execution of the generated AST.
	'''
	def __init__(self, fileInput=None):
		if fileInput is not None:
			self.loadFile(fileInput)
		self.global_symbols = {}
		self.symbol_scope_list = [[]]

	def run(self):
		return self.ast.run(self)

	def loadFile(self,filename):
		f = open(filename,"rb")
		self.ast = pickle.load(f)
		f.close()

