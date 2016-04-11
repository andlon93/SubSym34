import random as rng
import numpy as np
import matplotlib.pyplot as plt
import FlatLandEA as FL
import AdultSelection as AS
import ParentSelection as PS
import Crossover as C
import Game as G
import copy
import multiprocessing as mp
import win32api,win32process,win32con
pid = win32api.GetCurrentProcessId()
handle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, True, pid)
win32process.SetPriorityClass(handle, win32process.BELOW_NORMAL_PRIORITY_CLASS)

def gen_new_board():
	new_game = G.game()
	new_game.generateBoard((1/3),(1/3),10)
	global default_game
	default_game = copy.deepcopy(new_game)
	return copy.deepcopy(new_game)

#Global variables:

static = False
test_5 = True

default_game = None
gen_new_board()


###
def find_best_individual(gen):
	best_fitness = -1000
	best_individual = None
	for individual in gen:
		#individual.update_fitness(default_game) #remove this when working
		if individual.fitness > best_fitness:
			best_individual = individual
			best_fitness = individual.fitness
	return best_individual

def calculate_avg_std(survivors):

	# --- Calculate average fitness.
	avg_fitness = 0
	for survivor in survivors:
		avg_fitness += survivor.fitness
	avg_fitness = avg_fitness/len(survivors)

	# --- Calculate standard deviation of fitness.
	std_fitness = 0
	for survivor in survivors:
		std_fitness += (survivor.fitness - avg_fitness)**2
	std_fitness = np.sqrt(std_fitness/(len(survivors)-1))

	return avg_fitness, std_fitness
#
def temp_up_fit_5_stat(child,q,game):
	q.put(child.update_fitness(game))

def update_fitness_5_stat(children):
	boards = [0 for x in range(5)]
	k = [None] * 5
	q = mp.Queue()

	for i in range(5):
		boards[i] = gen_new_board()

	for child in children:
		tempval = 0
		for i in range(5):
			k[i] = mp.Process(target=temp_up_fit_5_stat, args=(child,q,boards[i]))
			k[i].start()
		for i in range(5):
			tempval += q.get().fitness
		for i in range(5):
			k[i].join()
		child.fitness = tempval / 5

def temp_up_fit_5_dyn(child,q):
	q.put(child.update_fitness(gen_new_board()))

def update_fintess_5_dyn(children):
	k = [None] * 5
	q = mp.Queue()
	for child in children:
		tempval = 0
		for i in range(5):
			k[i] = mp.Process(target=temp_up_fit_5_dyn, args=(child,q,))
			k[i].start()
		for i in range(5):
			tempval += q.get().fitness
		for i in range(5):
			k[i].join()
		child.fitness = tempval / 5



def update_fitness_individ(children,q,game):
	import win32api,win32process,win32con
	pid = win32api.GetCurrentProcessId()
	handle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, True, pid)
	win32process.SetPriorityClass(handle, win32process.BELOW_NORMAL_PRIORITY_CLASS)
	for child in children:
		child.update_fitness(game)
		q.put(child)

def EA_Loop(scaling, p_selection, adult_alg, pop_size, generation_limit, NSplits, Crossover_rate, mutation_rate, layers):
	# Initialise first child pool. mutate to pheno. fitness calc.

	# --- Initialise population with random candidate solutions.
	children = []
	survivors = []
	parents = []

	# for i in range(pop_size):
	# 	new_individual = FL.individual(mutation_rate, layers)
	# 	new_individual.update_fitness(default_game)
	# 	survivors.append(new_individual)

	# MULTIPROCESSING START
	number_of_cores = mp.cpu_count()
	q = mp.Queue()
	k = [None] * number_of_cores
	temp_childs = [None] * number_of_cores
	for i in range (number_of_cores):
		temp_childs[i] = []
	for i in range(pop_size):
		new_individual = FL.individual(mutation_rate, layers)
		survivors.append(new_individual)
	for i in range (len(survivors)):
		temp_childs[i%number_of_cores].append(survivors[i])
	for i in range(number_of_cores):
		k[i] = mp.Process(target=update_fitness_individ, args=(temp_childs[i],q,default_game,) )
		k[i].start()
	updated_children = []
	for i in range (len(survivors)):
		updated_children.append(q.get())
	for i in range(number_of_cores):
		k[i].join()
	survivors = updated_children
	# MULTIPROCESSING END


	# --- Initialize generation count.
	Ngenerations = 1

	# --- Find best individual in population.
	best_individual = find_best_individual(survivors)
	print("Antall mat: ", default_game.food_count, "Antall gift: ", default_game.poison_count)
	print ("Best initial individual fitness: ", best_individual.fitness)

	# Plot the best score in each generation
	plotting = [best_individual.fitness]
	plotting2 = [calculate_avg_std(survivors)[0]]
	#print("#", Ngenerations, " --- Best individual:\n", "Fitness: ", best_individual.fitness, "Genotype: ", best_individual.genotype)

	# --- Run as long as the best individual has fitness below 1.
	#while (best_individual.fitness < default_game.food_count and Ngenerations < generation_limit):
	while (Ngenerations < generation_limit): #best fitness changes when dynamic board

			#print ("New board - dynamic")
		# --- Update generation count.
		Ngenerations += 1

		# --- Make N children from the survivors of the previous generation.
		#     Select parents.
		#     Recombine pairs of parents.
		#     Mutate the resulting offspring.
		print("Generation: ", Ngenerations)
		children = C.make_children(survivors, pop_size, NSplits, Crossover_rate, p_selection, scaling)

		if test_5:
			if static:
				update_fitness_5_stat(children)
			if not static:
				print("DYNAMIC")
				for child in children:
					tempval = 0
					for i in range(5):
						child.update_fitness(gen_new_board())
						tempval += child.fitness
					child.fitness = tempval / 5
		else:
			if not static:
				gen_new_board()
			for child in children:
				child.update_fitness(default_game)

		for i in range(10):
			new_individual = FL.individual(mutation_rate, layers)
			new_individual.update_fitness(default_game)
			children.append(new_individual)
		#print("children made")
		# --- Select individuals for the next generation.
		#     N of the best individuals survive (fitness biased).
		#print("choosing parents...")
		survivors = adult_alg(children, parents, pop_size)

		# --- Calculate average fitness and standard deviation of fitness.
		avg_fitness, std_fitness = calculate_avg_std(survivors)

		# --- Find best individual in population.
		best_individual = find_best_individual(survivors)

		#SHOW A DEMO GAME MAYBE HERE???



		best_individual.save_game_log(default_game,"test.txt")

		# --- For plotting
		plotting.append(best_individual.fitness)
		plotting2.append(calculate_avg_std(survivors)[0])

		# --- Logging.
		#print("Antall mat: ", default_game.food_count, "Antall gift: ", default_game.poison_count)
		#print (Ngenerations,",",best_individual.fitness,",",avg_fitness,",",std_fitness)
		#if Ngenerations%2==0: print("#", Ngenerations, "\nBest individual --- ", "Fitness: ", best_individual.fitness, "\nGenotype: ", best_individual.genotype, "\nAverage of fitness: ", avg_fitness, ". Standard deviation of fitness: ", std_fitness, ".\n")
		#print("#", Ngenerations, "\nBest individual --- ", "Fitness: ", best_individual.fitnesstness, "\nGenotype: ", best_individual.genotype, "\nAverage of fitness: ", avg_fitness, ". Standard deviation of fitness: ", std_fitness, ".\n")
		#if best_individual.fitness == default_game.food_count: print("#", Ngenerations, "\t Best individual is optimized!")
	#
	print ("DONE")
	#if static:
	print ("Generating new board to best best individual")
	gen_new_board()
	best_individual.update_fitness(default_game)
	best_individual.save_game_log(default_game,"StaticOneRun.txt")
	print ("Total food on new board: ",default_game.food_count)
	print ("Fitness of best on new board: ",best_individual.fitness)

	if Ngenerations%10==0: print("#", Ngenerations, "\nBest individual --- ", "Fitness: ", best_individual.fitness, "\nGenotype: ", best_individual.genotype)
	#if Choose_problem>1: print("Fitness: ",best_individual.fitness,"\nSequence: ", best_individual.genotype)
	if (best_individual.fitness == default_game.food_count): return Ngenerations, True, plotting, plotting2
	else: return Ngenerations, False, plotting, plotting2
	#return Ngenerations
#
def main():
	#Choose_problem = 3 # 0==OneMax, 1==LOLZ, 2==LocalSS, 3==GlobalSS
	#adult_alg = 0 # 0==full repl., 1==over prod., 2==Gen. mixing
	#parent_alg = 0 # 0==Global, 1==tournament
	#scaling = 3 # 0==fitness_prop, 1==sigma, 2==boltzmann, 3==rank
	#
	#z = 21
	#s = 15
	#
	N = 1
	sum_generations = 0
	std_generations = 0
	Nfails = 0
	#
	gen_limit = 100000
	#pop_size = 230
	NSplits = 5
	#Crossover_rate = 0.8
	#mutation_rate = 0.0001
	#bit_length = 37
	#
	#
	#plotting=[[]]*100
	#
	Gen = 20
	Ngenerations, isDone, plots, plots2 = EA_Loop(PS.rank_scaling , PS.Tournament_Selection, AS.Generational_Mixing, 100, Gen,1, 0.5, 0.01, [6,3])
	'''
	for i in range(N):
		if adult_alg==0:
			if parent_alg==0:
				if scaling==0:Ngenerations, isDone, plots, plots2 = EA_Loop(PS.fitness_proportionate_scaling , PS.Global_Selection, AS.Full_Generational_Replacement, Choose_problem, z, s, pop_size, gen_limit, NSplits, Crossover_rate, mutation_rate, bit_length)
				elif scaling==1:Ngenerations, isDone, plots, plots2 = EA_Loop(PS.sigma_scaling , PS.Global_Selection, AS.Full_Generational_Replacement, Choose_problem, z, s, pop_size, gen_limit, NSplits, Crossover_rate, mutation_rate, bit_length)
				elif scaling==2:Ngenerations, isDone, plots, plots2 = EA_Loop(PS.boltzmann_scaling , PS.Global_Selection, AS.Full_Generational_Replacement, Choose_problem, z, s, pop_size, gen_limit, NSplits, Crossover_rate, mutation_rate, bit_length)
				else:Ngenerations, isDone, plots, plots2 = EA_Loop(PS.rank_scaling , PS.Global_Selection, AS.Full_Generational_Replacement, Choose_problem, z, s, pop_size, gen_limit, NSplits, Crossover_rate, mutation_rate, bit_length)
			else:
				if scaling==0:Ngenerations, isDone, plots, plots2 = EA_Loop(PS.fitness_proportionate_scaling , PS.Tournament_Selection, AS.Full_Generational_Replacement, Choose_problem, z, s, pop_size, gen_limit, NSplits, Crossover_rate, mutation_rate, bit_length)
				elif scaling==1:Ngenerations, isDone, plots, plots2 = EA_Loop(PS.sigma_scaling , PS.Tournament_Selection, AS.Full_Generational_Replacement, Choose_problem, z, s, pop_size, gen_limit, NSplits, Crossover_rate, mutation_rate, bit_length)
				elif scaling==2:Ngenerations, isDone, plots, plots2 = EA_Loop(PS.boltzmann_scaling , PS.Tournament_Selection, AS.Full_Generational_Replacement, Choose_problem, z, s, pop_size, gen_limit, NSplits, Crossover_rate, mutation_rate, bit_length)
				else:Ngenerations, isDone, plots, plots2 = EA_Loop(PS.rank_scaling , PS.Tournament_Selection, AS.Full_Generational_Replacement, Choose_problem, z, s, pop_size, gen_limit, NSplits, Crossover_rate, mutation_rate, bit_length)
		elif adult_alg==1:
			if parent_alg==0:
				if scaling==0:Ngenerations, isDone, plots, plots2 = EA_Loop(PS.fitness_proportionate_scaling , PS.Global_Selection, AS.Full_Generational_Replacement, Choose_problem, z, s, pop_size, gen_limit, NSplits, Crossover_rate, mutation_rate, bit_length)
				elif scaling==1:Ngenerations, isDone, plots, plots2 = EA_Loop(PS.sigma_scaling , PS.Global_Selection, AS.Full_Generational_Replacement, Choose_problem, z, s, pop_size, gen_limit, NSplits, Crossover_rate, mutation_rate, bit_length)
				elif scaling==2:Ngenerations, isDone, plots, plots2 = EA_Loop(PS.boltzmann_scaling , PS.Global_Selection, AS.Full_Generational_Replacement, Choose_problem, z, s, pop_size, gen_limit, NSplits, Crossover_rate, mutation_rate, bit_length)
				else:Ngenerations, isDone, plots, plots2 = EA_Loop(PS.rank_scaling , PS.Global_Selection, AS.Full_Generational_Replacement, Choose_problem, z, s, pop_size, gen_limit, NSplits, Crossover_rate, mutation_rate, bit_length)
			else:
				if scaling==0:Ngenerations, isDone, plots, plots2 = EA_Loop(PS.fitness_proportionate_scaling , PS.Tournament_Selection, AS.Full_Generational_Replacement, Choose_problem, z, s, pop_size, gen_limit, NSplits, Crossover_rate, mutation_rate, bit_length)
				elif scaling==1:Ngenerations, isDone, plots, plots2 = EA_Loop(PS.sigma_scaling , PS.Tournament_Selection, AS.Full_Generational_Replacement, Choose_problem, z, s, pop_size, gen_limit, NSplits, Crossover_rate, mutation_rate, bit_length)
				elif scaling==2:Ngenerations, isDone, plots, plots2 = EA_Loop(PS.boltzmann_scaling , PS.Tournament_Selection, AS.Full_Generational_Replacement, Choose_problem, z, s, pop_size, gen_limit, NSplits, Crossover_rate, mutation_rate, bit_length)
				else:Ngenerations, isDone, plots, plots2 = EA_Loop(PS.rank_scaling , PS.Tournament_Selection, AS.Full_Generational_Replacement, Choose_problem, z, s, pop_size, gen_limit, NSplits, Crossover_rate, mutation_rate, bit_length)
		else:
			if parent_alg==0:
				if scaling==0:Ngenerations, isDone, plots, plots2 = EA_Loop(PS.fitness_proportionate_scaling , PS.Global_Selection, AS.Full_Generational_Replacement, Choose_problem, z, s, pop_size, gen_limit, NSplits, Crossover_rate, mutation_rate, bit_length)
				elif scaling==1:Ngenerations, isDone, plots, plots2 = EA_Loop(PS.sigma_scaling , PS.Global_Selection, AS.Full_Generational_Replacement, Choose_problem, z, s, pop_size, gen_limit, NSplits, Crossover_rate, mutation_rate, bit_length)
				elif scaling==2:Ngenerations, isDone, plots, plots2 = EA_Loop(PS.boltzmann_scaling , PS.Global_Selection, AS.Full_Generational_Replacement, Choose_problem, z, s, pop_size, gen_limit, NSplits, Crossover_rate, mutation_rate, bit_length)
				else:Ngenerations, isDone, plots, plots2 = EA_Loop(PS.rank_scaling , PS.Global_Selection, AS.Full_Generational_Replacement, Choose_problem, z, s, pop_size, gen_limit, NSplits, Crossover_rate, mutation_rate, bit_length)
			else:
				if scaling==0:Ngenerations, isDone, plots, plots2 = EA_Loop(PS.fitness_proportionate_scaling , PS.Tournament_Selection, AS.Full_Generational_Replacement, Choose_problem, z, s, pop_size, gen_limit, NSplits, Crossover_rate, mutation_rate, bit_length)
				elif scaling==1:Ngenerations, isDone, plots, plots2 = EA_Loop(PS.sigma_scaling , PS.Tournament_Selection, AS.Full_Generational_Replacement, Choose_problem, z, s, pop_size, gen_limit, NSplits, Crossover_rate, mutation_rate, bit_length)
				elif scaling==2:Ngenerations, isDone, plots, plots2 = EA_Loop(PS.boltzmann_scaling , PS.Tournament_Selection, AS.Full_Generational_Replacement, Choose_problem, z, s, pop_size, gen_limit, NSplits, Crossover_rate, mutation_rate, bit_length)
				else:Ngenerations, isDone, plots, plots2 = EA_Loop(PS.rank_scaling , PS.Tournament_Selection, AS.Full_Generational_Replacement, Choose_problem, z, s, pop_size, gen_limit, NSplits, Crossover_rate, mutation_rate, bit_length)'''
		#if not isDone:Nfails += 1
		#sum_generations += Ngenerations
		#std_generations += (Ngenerations - sum_generations/(i+1))**2
		#if i%50==0:
		#	print("\nRuns: ", i+1)
		#	print("Number of fails: ", Nfails)
		#for i in range(len(plots)):
		#	plotting[i].append(plots[i])
	# --- Logging data for all the generations.
	#print('Average number of generations = ', sum_generations/N, ' Standard deviation of number of generations ~ ', np.sqrt(std_generations/(N-1)))
	#print('#fails: ', Nfails, ' / ', i+1, ' = ', Nfails/(i+1)*100, '%\n')
	#return plots


	# --- Plotting
	plt.plot(range(1,len(plots)+1), plots, label='best individual')
	plt.plot(range(1,len(plots2)+1), plots2, label='average in population')
	plt.legend(loc='lower right')
	plt.xlabel('Number of generations')
	plt.ylabel('Fitness')
	plt.axis([0, len(plots), 0, 1.1])
	plt.show()
#
def run():
	not_done="1"
	while not_done=="1":
		z=0
		s=0
		print("Choose problem: 0=One Max, 1=LOLZ, 2=localSS, 3=globalSS")
		problem=input("input int: ")
		if problem=="0":
			bit_size = input("input bit length: ")
		if problem=="1":
			bit_size = input("input bit length: ")
			z=input("Z: ")
		elif problem == "2" or problem == "3":
			s=input("S: ")
			bit_size=input("L: ")
		pop_size=input("Population Size: ")
		Crossover_rate=input("Crossover rate: ")
		mutation_rate=input("Mutation rate: ")
		#
		print("Choose adult alg: 0=full repl., 1=over prod., 2=gen. mixing")
		adult_alg=input("input int: ")
		#
		print("parent selection: 0=tournament, 1=fitness prop., 2=sigma, 3=rank")
		p_select=input("input int: ")
		if p_select=="0":
			parent_alg=1
			scaling=0
		elif p_select=="1":
			parent_alg=0
			scaling=0
		elif p_select=="2":
			parent_alg=0
			scaling=1
		else:
			parent_alg=0
			scaling=3

		main(int(problem), int(bit_size), int(z), int(s), int(pop_size), float(Crossover_rate), float(mutation_rate), int(adult_alg), int(parent_alg), int(scaling))

		not_done=input("Do you wish to continue(1/0)? ")
		#
#
if __name__ == '__main__':
	#       scaling, p_selection, adult_alg, pop_size, generation_limit, NSplits, Crossover_rate, mutation_rate, layers)
	#EA_Loop(PS.rank_scaling , PS.Tournament_Selection, AS.Full_Generational_Replacement, 100, 100,2, 0.2, 0.01, [6,3])
	#EA_Loop(PS.rank_scaling , PS.Tournament_Selection, AS.Full_Generational_Replacement, 100, 100,2, 0.4, 0.1, [6,3])
	#Crossover_rate = 0.8
	#mutation_rate = 0.0001
	#print("\n--- Tournament: eps:0.05 k=64")
	s=main()
	#print("Global.\nS:15 bit:37")
	'''j=1
	temp=[]
	for mnb in range(j):
		p=main(1,0)
		print("tournament: ", mnb)
		temp.append(p)
	p1=[]
	for i in range(100):
		for n in range(j):
			s=0.0
			t=0.0
			#print(len(temp[n]), i)
			if len(temp[n]) > i:
				s+=temp[n][i]
				t+=1.0
		if (t>0.0):
			#print("append")
			p1.append( s/t )
	print("en ferdig----------------------------------------------------------------------------------------------")
	temp=[]
	for mnb in range(j):
		p=main(0,0)
		print("fitness prop: ", mnb)
		temp.append(p)
	p2=[]
	for i in range(100):
		for n in range(j):
			s=0.0
			t=0.0
			if len(temp[n]) > i:
				s+=temp[n][i]
				t+=1.0
		if (t>0.0):
			p2.append( s/t )
	#
	print("to ferdig----------------------------------------------------------------------------------------------")
	temp=[]
	for mnb in range(j):
		p=main(0,1)
		print("Sigma: ", mnb)
		temp.append(p)
	p3=[]
	for i in range(100):
		for n in range(j):
			s=0.0
			t=0.0
			if len(temp[n]) > i:
				s+=temp[n][i]
				t+=1.0
		if (t>0.0):
			p3.append( s/t )

	#temp=[]
	#for mnb in range(j):
#		p=main(0,2)
#		temp.append(p)
#	p4=[]
#	for i in range(100):
#		for n in range(j):
#			s=0.0
#			t=0.0
###				t+=1.0
	#	if (t>0.0):
	#		p4.append( s/t )
	print("tre ferdig----------------------------------------------------------------------------------------------")
	temp=[]
	for mnb in range(j):
		p=main(0,3)
		print("Rank: ", mnb)
		temp.append(p)
	p5=[]
	for i in range(100):
		for n in range(j):
			s=0.0
			t=0.0
			if len(temp[n]) > i:
				s+=temp[n][i]
				t+=1.0
		if (t>0.0):
			p5.append( s/t )
	#
	plt.plot(range(1,len(p1)+1), p1, label='Tournament')
	plt.plot(range(1,len(p2)+1), p2, label='Fitness proportionate')
	plt.plot(range(1,len(p3)+1), p3, label='Sigma scaling')
	#plt.plot(range(1,len(p4)+1), p4)#, label='Boltzmann scaling')
	plt.plot(range(1,len(p5)+1), p5, label='Rank scaling')
	#plt.plot(range(1,len(p6)+1), p6)#, label='Rank scaling')
	#plt.plot(range(1,len(p7)+1), p7)#, label='Rank scaling')
	#plt.plot(range(1,len(p8)+1), p8)#, label='Rank scaling')
	plt.legend(loc='lower right')
	plt.xlabel('Number of generations')
	plt.ylabel('Fitness')
	plt.axis([0, 100, 0.95*min(p1[0],p2[0],p3[0],p5[0]), 1.05])
	plt.show()'''

	'''pop_size = 220
	while pop_size < 300:
		print("\n--- Population size: ",pop_size)
		pop_size += 20'''