import random as rng
import NN
#
class individual:
	genotype           = None
	phenotype          = None
	mutation_prob      = None
	game               = None
	normalised_fitness = 0
	fitness            = 0

	def __init__(self, mutation_prob, layers, game, genotype=None):
		self.mutation_prob = mutation_prob
		self.genotype = genotype
		if self.genotype==None:
			#print(layers)
			self.makeRandomGenotype(layers)
		self.update_fitness()
	#
	def makeRandomGenotype(self, layers):
		#self.genotype.append( [ [None]*layers[i] ]*layers[i+1] )
		self.genotype = []
		#print(len(layers))
		for i in range(len(layers)-1):
			temp1=[]
			for j in range(layers[i]):
				temp2=[]
				for k in range(layers[i+1]):
					temp2.append(rng.random())
				temp1.append(temp2)
			self.genotype.append(temp1)
	#
	def __repr__(self):
		return str(self.fitness)
	#
	def try_to_mutate(self):
		is_mutated=False
		if rng.random() < self.mutation_prob:
			is_mutated=True
			t=rng.randint(0,len(self.genotype)-1)
			u=rng.randint(0,len(self.genotype[t])-1)
			v=rng.randint(0,len(self.genotype[t][u])-1)
			self.genotype[t][u][v] = rng.random()
			self.update_fitness()
		return is_mutated
	#
	def update_fitness(self):
		network = NN.NN(self.genotype)
		for i in range(50):
			self.game.move(NN.forward_propagation(self.game.getNearbyTiles()))
		self.fitness = self.game.evalFitness()





if __name__ == '__main__':
	n=individual(0.2,[2,2])
	print(n.genotype)
	n.try_to_mutate()
	print(n.genotype)