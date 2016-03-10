import random as rng
import ParentSelection as PS
import numpy as np
import copy
import FlatLandEA as FL
### Function that: Make children based on two genotypes
	#	Input:         two genotypes
	#   Outout:        Children(new genotypes)
def One_Point_Crossover(female, male):
	# Number to split the genomes on
	split = rng.randint(0, len(female.genotype)-1)

	# Splitting the females genome on the split number
	female_genome_1 = female.genotype[:split]
	female_genome_2 = female.genotype[split:]

	# Splitting the males genome on the split number
	male_genome_1 = male.genotype[:split]
	male_genome_2 = male.genotype[split:]

	'''
	print(split)
	print("Female:\n",female.genotype,"\n",female_genome)
	print("\n\nMale:\n",male.genotype,"\n", male_genome)
	print(female_genome+male_genome)
	child =  OM.individual(female.genotype_Length, female.mutation_prob, female_genome+male_genome)
	print(child.genotype)
	'''
	m=male.mutation_prob
	child1 = FL.individual(m, None, female_genome_1+male_genome_2)
	child2 = FL.individual(m, None, male_genome_1+female_genome_2)
	# Returning the new genotypes combined from the two parents
	return child1, child2

	### Function that: Make children based on two genotypes
	#	Input:         two genotypes
	#   Outout:        Children(new genotypes)
def N_Point_Crossover(parents, Nsplits):

	Ngenes = len(parents[0].genotype)
	mutation_prob = parents[0].mutation_prob
	splits = rng.sample(range(1, Ngenes), Nsplits)
	splits.append(0)
	splits.append(Ngenes)
	splits = sorted(splits)

	genome1 = []
	genome2 = []

	for i in range(len(splits)-1):
		genome1 = genome1 + parents[i%2].genotype[splits[i]:splits[i+1]]
		genome2 = genome2 + parents[i%2-1].genotype[splits[i]:splits[i+1]]
	m=parents[0].mutation_prob
	child1 = FL.individual(m, None, genome1)
	child2 = FL.individual(m, None, genome2)

	# Returning the new genotypes combined from the two parents
	return child1, child2

def make_children(adults, children_size, Nsplits, p, p_selection, scaling):
	children = []
	# --- Select two random parents and make a child until
	#     number of children equals children_size.
	while (len(children) < children_size):
		#print(len(children))
		#p = 1.0
		#Nsplits = 5

		# --- Find parents.
		parents = p_selection(scaling, adults, 2, 0.05, 24)
		#print(parents[0].genotype)
		#if p_selection==0: parents = PS.Global_Selection(scaling, adults, 2)
		#else: parents = PS.Tournament_Selection()

		# --- Make children.
		if (rng.random() < p):
			child1, child2 = One_Point_Crossover(parents[0], parents[1])
			#child1, child2 = N_Point_Crossover(parents, Nsplits)
		else:
			child1 = parents[0]
			child2 = parents[1]

		# --- Possible mutation.
		child1.try_to_mutate()
		child2.try_to_mutate()
		# --- Append children to list of children.
		children.append(child1)
		if len(children) < children_size:
			children.append(child2)

	#print("children: ",children)
	return children



if __name__ == '__main__':
	import OneMax as OM
	male = OM.individual(10, 0.05)
	female = OM.individual(10, 0.05)
	Two_Point_Crossover(female, male)