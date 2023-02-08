from solution import SOLUTION
import constants as c
import copy
import os

class PARALLEL_HILL_CLIMBER:

	def __init__(self):
		os.system("rm brain*.nndf")
		os.system("rm fitness*.txt")

		self.nextAvailableID = 0
		self.parents = {}

		for populationID in range(c.populationSize):
			self.parents[populationID] = SOLUTION(self.nextAvailableID, populationID)
			self.nextAvailableID += 1

	def Evolve(self):

		self.Evaluate(self.parents)

		for currentGeneration in range(c.numberOfGenerations):
			self.Evolve_For_One_Generation()

	def Evolve_For_One_Generation(self):
		self.Spawn()
		self.Mutate()
		self.Evaluate(self.children)
		self.Print()
		self.Select()

	def Spawn(self):
		self.children = {}

		for key in self.parents:
			self.children[key] = copy.deepcopy(self.parents[key])
			self.children[key].Set_ID(self.nextAvailableID)
			self.nextAvailableID += 1

	def Mutate(self):
		for key in self.children:
			self.children[key].Mutate()

	def Evaluate(self, solutions):
		for key in self.parents:
			solutions[key].Start_Simulation("DIRECT")

		for key in self.parents:
			solutions[key].Wait_For_Simulation_To_End()

	def Select(self):
		for key in self.parents:
			if self.parents[key].fitness > self.children[key].fitness: # If the parent does worse, since more negative is better
				self.parents[key] = self.children[key]

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

		self.parents[fittest].Start_Simulation("GUI")