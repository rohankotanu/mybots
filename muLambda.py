from solution import SOLUTION
import constants as c
import numpy as np
import pickle
import copy
import os

class MU_LAMBDA:

	def __init__(self):
		os.system("rm brain*.nndf")
		os.system("rm body*.urdf")
		os.system("rm fitness*.txt")

		self.nextAvailableID = 0
		self.nextAvailableOriginID = 0
		self.population = []

		for i in range(c.populationSize):
			self.population += [SOLUTION(self.nextAvailableID, self.nextAvailableOriginID, 0, 0)]
			self.nextAvailableID += 1
			self.nextAvailableOriginID += 1

		self.fitness_over_time = np.empty([1, 5])

	def Evolve(self):
		for currentGeneration in range(c.numberOfGenerations):
			self.Evolve_For_One_Generation(currentGeneration)

		self.Evaluate(self.population, c.numberOfGenerations)


	def Evolve_For_One_Generation(self, currentGeneration):
		self.Evaluate(self.population, currentGeneration)
		self.Print()
		self.Select(currentGeneration)
		self.Spawn(currentGeneration)

	def Spawn(self, currentGeneration):

		new_population = []

		for individual in self.population:
			individual.age += 1
			new_population += [individual]

			for i in range(int(c.populationSize/c.mu - 2)):
				child = copy.deepcopy(individual)
				child.Set_ID(self.nextAvailableID)
				child.populationID = self.nextAvailableOriginID

				data = np.array([[currentGeneration, self.nextAvailableOriginID, individual.generationCreated, individual.age-1, -individual.fitness]])
				self.fitness_over_time = np.append(self.fitness_over_time, data, axis=0)

				self.nextAvailableID += 1
				self.nextAvailableOriginID += 1
				child.Mutate()

				new_population += [child]

		for i in range(c.mu):
			child = SOLUTION(self.nextAvailableID, self.nextAvailableOriginID, currentGeneration, 0)
			self.nextAvailableID += 1
			self.nextAvailableOriginID += 1

			new_population += [child]

		self.population = new_population
			

	def Mutate(self):
		for key in self.children:
			self.children[key].Mutate()

	def Evaluate(self, solutions, currentGeneration):
		print("Generaton " + str(currentGeneration) + ":")
		for sol in solutions:
			sol.Start_Simulation("DIRECT")

		for sol in solutions:
			sol.Wait_For_Simulation_To_End()

		for i in range(len(self.population)):
			data = np.array([[currentGeneration, self.population[i].populationID, self.population[i].generationCreated, self.population[i].age, -self.population[i].fitness]])
			self.fitness_over_time = np.append(self.fitness_over_time, data, axis=0)

	def Select(self, currentGeneration):
		fitnesses = []

		# Generate a sorted list of fitnesses
		for i in range(c.populationSize):
			fitnesses += [self.population[i].fitness]

		fitnesses.sort(key = float)

		# Only keep top parents (depends on value of mu)
		self.population = [individual for individual in self.population if individual.fitness <= fitnesses[c.mu-1]]

	def Print(self):
		print("\n")

		for individual in self.population:
			print(f"Fitness: {individual.fitness}")

		print("\n")

	def Show_Best(self):
		# Find fittest parent
		fittest = self.population[0]

		for individual in self.population:
			print(individual.populationID, individual.age)
			if individual.fitness < fittest.fitness:
				fittest = individual

		# Save fittest solution and show simulation in GUI
		pickle.dump(fittest, open( "fittest.p", "wb" ) )
		fittest.Start_Simulation("GUI")