import numpy as np
from scipy.stats import logistic
#
class NN:
	weights = None
	#
	def __init__(self, weights):
		self.weights = np.asarray(weights)
	#
	def sigmoid(self, x):
		return logistic.cdf(x)
	#
	def soft_max(self, x):
		return x
	#
	def forward_propagation(self, innput):
		innput = np.asarray(innput)
		for weight in self.weights:
			innput = np.dot(innput,weight)
			# Run activation function
			for i in range(len(innput)):
				innput[i] = self.sigmoid(innput[i])
			#
		output = self.soft_max(innput)
		print(output)
		return np.argmax(output)
if __name__ == '__main__':
	import Game as G
	import FlatLandEA as FL
	fl = FL.individual(0.1, [6,3])
	print(fl.genotype)
	nn = NN(fl.genotype)
	print( nn.forward_propagation( [1,1,1,1,1,1] ) )
	