from parser import *
import pickle

class VirtualMachine():
	def __init__(self, fileInput=None):
		if fileInput is not None:
			self.ast = self.loadFile(fileInput)
		self.global_symbols = {}
		self.symbol_scope_list = []

	def run(self):
		return self.ast.run(self)

	def loadFile(self,filename):
		self.ast = pickle.load(filename)
