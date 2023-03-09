from solution import SOLUTION
import constants as c
import numpy as np
import pickle
import copy
import os

class PARALLEL_HILL_CLIMBER:

	def __init__(self):
		os.system("rm brain*.nndf")
		os.system("rm body*.urdf")
		os.system("rm fitness*.txt")

		self.nextAvailableID = 0
		self.parents = {}

		for populationID in range(c.populationSize):
			self.parents[populationID] = SOLUTION(self.nextAvailableID, 0, 0, 0)
			self.nextAvailableID += 1

		self.fitness_over_time = np.zeros((c.populationSize, c.numberOfGenerations))

	def Evolve(self):

		self.Evaluate(self.parents, 0)

		for currentGeneration in range(c.numberOfGenerations):
			self.Evolve_For_One_Generation(currentGeneration)

	def Evolve_For_One_Generation(self, currentGeneration):
		self.Spawn()
		self.Mutate()
		self.Evaluate(self.children, currentGeneration)
		self.Print()
		self.Select(currentGeneration)

	def Spawn(self):
		self.children = {}

		for key in self.parents:
			self.children[key] = copy.deepcopy(self.parents[key])
			self.children[key].Set_ID(self.nextAvailableID)
			self.nextAvailableID += 1

	def Mutate(self):
		for key in self.children:
			self.children[key].Mutate()

	def Evaluate(self, solutions, currentGeneration):
		print("Generaton " + str(currentGeneration) + ":")
		for key in solutions:
			solutions[key].Start_Simulation("DIRECT")

		for key in solutions:
			solutions[key].Wait_For_Simulation_To_End()

	def Select(self, currentGeneration):
		for populationID in self.parents:
			if self.parents[populationID].fitness > self.children[populationID].fitness: # If the parent does worse, since more negative is better
				self.parents[populationID] = self.children[populationID]
				self.fitness_over_time[populationID][currentGeneration] = -self.children[populationID].fitness
			else:
				self.fitness_over_time[populationID][currentGeneration] = -self.parents[populationID].fitness

	def Print(self):
		print("\n")

		for key in self.parents:
			print(f"Parent's fitness: {self.parents[key].fitness}, Child's fitness: {self.children[key].fitness}")

		print("\n")

	def Show_Best(self):
		# Find fittest parent
		fittest = 0
		best_fitness = self.parents[0].fitness

		for key in self.parents:
			if self.parents[key].fitness < best_fitness:
				best_fitness = self.parents[key].fitness
				fittest = key

		# Save fittest solution and show simulation in GUI
		pickle.dump(self.parents[fittest], open( "fittest.p", "wb" ) )
		self.parents[fittest].Start_Simulation("GUI")