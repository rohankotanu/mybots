from solution import SOLUTION
import constants as c
import numpy as np
import pickle
import math
import copy
import os

class AGE_FITNESS_PARETO:

	def __init__(self):
		os.system("rm brain*.nndf")
		os.system("rm body*.urdf")
		os.system("rm fitness*.txt")

		self.nextAvailableID = 0
		self.nextAvailableOriginID = 0
		self.population = []
		self.populationSize = []

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

			for i in range(1):
				child = copy.deepcopy(individual)
				child.Set_ID(self.nextAvailableID)
				child.populationID = self.nextAvailableOriginID

				data = np.array([[currentGeneration, self.nextAvailableOriginID, individual.generationCreated, individual.age-1, -individual.fitness]])
				self.fitness_over_time = np.append(self.fitness_over_time, data, axis=0)

				self.nextAvailableID += 1
				self.nextAvailableOriginID += 1
				child.Mutate()
				new_population += [child]

		for i in range(1):
			child = SOLUTION(self.nextAvailableID, self.nextAvailableOriginID, currentGeneration, 0)
			self.nextAvailableID += 1
			self.nextAvailableOriginID += 1
			new_population += [child]

		self.population = new_population
		self.populationSize += [len(self.population)]
			

	def Mutate(self):
		for key in self.children:
			self.children[key].Mutate()

	def Evaluate(self, solutions, currentGeneration):
		print("Generation " + str(currentGeneration) + ":")
		for sol in solutions:
			sol.Start_Simulation("DIRECT")

		for sol in solutions:
			sol.Wait_For_Simulation_To_End()

		for i in range(len(self.population)):
			data = np.array([[currentGeneration, self.population[i].populationID, self.population[i].generationCreated, self.population[i].age, -self.population[i].fitness]])
			self.fitness_over_time = np.append(self.fitness_over_time, data, axis=0)

	def Select(self, currentGeneration):
		fitnesses = []
		ages = []
		bestIndividuals = []

		# Generate a sorted list of fitnesses
		for i in range(len(self.population)):
			fitnesses += [self.population[i].fitness]
			ages += [self.population[i].age]

		paretoLevels = self.Get_Pareto_Levels(fitnesses, ages)

		pLevel = 0

		while len(bestIndividuals) < 12:
			for n in range(len(self.population)):
				if paretoLevels[n] == pLevel:
					bestIndividuals += [self.population[n]]

					if len(bestIndividuals) == 12:
						break

			pLevel += 1

		self.population = bestIndividuals

	def Print(self):
		print("\n")

		for individual in self.population:
			print(f"Fitness: {individual.fitness}")

		print("\n")

	def Get_Pareto_Levels(self, fitnesses, ages):
		pareto_levels = np.zeros(len(fitnesses))

		for i in range(len(fitnesses)):
			onParetoFront = True

			for k in range(len(fitnesses)):
				if fitnesses[k] < fitnesses[i] and ages[k] <= ages[i]:
					pareto_levels[i] += 1

		return pareto_levels

	def Show_Best(self):
		# Find fittest parent
		fittest = self.population[0]

		for individual in self.population:
			#print(individual.populationID, individual.age)
			if individual.fitness < fittest.fitness:
				fittest = individual

		# Save fittest solution and show simulation in GUI
		pickle.dump(fittest, open( "fittest.p", "wb" ) )
		fittest.Start_Simulation("GUI")