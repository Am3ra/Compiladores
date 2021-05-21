from parser import *
import pickle


class VirtualMachine():
	def __init__(self, fileInput=None):
		if fileInput is not None:
			self.loadFile(fileInput)
		self.global_symbols = {}
		self.symbol_scope_list = [[]]

	def run(self):
		# print(self.ast)
		return self.ast.run(self)

	def loadFile(self,filename):
		# os.open(filename)
		f = open(filename,"rb")
		self.ast = pickle.load(f)
		print(self.ast)
		f.close()

#with open('out/cache/' +hashed_url, 'rb') as pickle_file:
#   content = pickle.load(pickle_file)