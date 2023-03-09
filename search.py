import os
from parallelHillClimber import PARALLEL_HILL_CLIMBER
from muLambda import MU_LAMBDA
from ageFitnessPareto import AGE_FITNESS_PARETO
from matplotlib import pyplot as plt
import constants as c
import numpy as np
import sys

phc_or_ml = sys.argv[1]

if phc_or_ml == "phc":
	phc = PARALLEL_HILL_CLIMBER()
	phc.Evolve()
	phc.Show_Best()

	# Plot fitness data
	fitness_data = phc.fitness_over_time
	generations = np.arange(c.numberOfGenerations)
	plt.plot(generations, fitness_data[0])
	plt.plot(generations, fitness_data[1])
	plt.plot(generations, fitness_data[2])
	plt.plot(generations, fitness_data[3])
	plt.plot(generations, fitness_data[4])
	plt.plot(generations, fitness_data[5])
	plt.plot(generations, fitness_data[6])
	plt.plot(generations, fitness_data[7])
	plt.plot(generations, fitness_data[8])
	plt.plot(generations, fitness_data[9])
	plt.plot(generations, fitness_data[10])
	plt.plot(generations, fitness_data[11])
	plt.plot(generations, fitness_data[12])
	plt.plot(generations, fitness_data[13])
	plt.plot(generations, fitness_data[14])
	plt.plot(generations, fitness_data[15])
	plt.plot(generations, fitness_data[16])
	plt.plot(generations, fitness_data[17])
	plt.plot(generations, fitness_data[18])
	plt.plot(generations, fitness_data[19])
	plt.plot(generations, fitness_data[20])
	plt.plot(generations, fitness_data[21])
	plt.plot(generations, fitness_data[22])
	plt.plot(generations, fitness_data[23])
	plt.plot(generations, fitness_data[24])
	#plt.legend(['Population 1', 'Population 2', 'Population 3', 'Population 4', 'Population 5'], loc='upper left')
	plt.title('Fitness Over Time')
	plt.xlabel('Generation')
	plt.ylabel('Fitness (-x displacement)')
	plt.show()

elif phc_or_ml == "ml":
	ml = MU_LAMBDA()
	ml.Evolve()
	ml.Show_Best()

	populationIDs = list(set(ml.fitness_over_time[:,1]))

	for populationID in populationIDs:
		lineage = ml.fitness_over_time[np.where(ml.fitness_over_time[:,1] == populationID)]

		x = []
		y = []

		for row in lineage:
			x += [row[2] + row[3]]
			y += [row[4]]

		plt.plot(x, y)

	plt.title('Fitness Over Time')
	plt.xlabel('Generation')
	plt.ylabel('Fitness (-x displacement)')
	plt.show()

elif phc_or_ml == "afpo":
	afpo = AGE_FITNESS_PARETO()
	afpo.Evolve()
	afpo.Show_Best()


	populationIDs = list(set(afpo.fitness_over_time[:,1]))

	for populationID in populationIDs:
		lineage = afpo.fitness_over_time[np.where(afpo.fitness_over_time[:,1] == populationID)]

		x = []
		y = []

		for row in lineage:
			x += [row[2] + row[3]]
			y += [row[4]]

		plt.plot(x, y)

	plt.title('Fitness Over Time')
	plt.xlabel('Generation')
	plt.ylabel('Fitness (-x displacement)')
	plt.show()
	# plt.scatter(afpo.fitness_over_time[:,0], afpo.fitness_over_time[:,2], c=afpo.fitness_over_time[:, 1], cmap='tab10')
	# plt.title('Fitness Over Time')
	# plt.xlabel('Generation')
	# plt.ylabel('Fitness (-x displacement)')
	# plt.show()

	# plt.plot(np.arange(len(afpo.populationSize)), afpo.populationSize)
	# plt.title('Fitness Over Time')
	# plt.xlabel('Generation')
	# plt.ylabel('Fitness (-x displacement)')
	# plt.show()