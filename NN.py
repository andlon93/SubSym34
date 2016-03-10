import numpy as np
#
class NN:
	weights = None
	#
	def __init__(self, weights):
		self.weights = np.asarray(weights)
	#
	def sigmoid(self):
		pass
	#
	def soft_max(self):
		pass
	#
	def forward_propagation(innput, a_Func, soft_max):
		innput = np.asarray(innput)
		for weight in weights:
			innput = np.dot(innput,weight)
			# Run activation function
			for i in range(len(temp)):
				innput[i] = a_Func(innput[i])
			#
		output = soft_max(temp)




		