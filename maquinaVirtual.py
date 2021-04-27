from parser import *

class VirtualMachine():
	def __init__(self, fileInput):
		self.file = fileInput
		self.global_symbols = {}
		self.symbol_scope_list = []

	def run(self):
		self.ast.run(self)
