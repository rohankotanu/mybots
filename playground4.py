import numpy as np
from matplotlib import pyplot as plt

def GetParetoFront(fitness, age):
	pareto_fitnesses = np.zeros(len(fitness))

	for i in range(len(fitness)):
		onParetoFront = True

		for k in range(len(fitness)):
			if fitness[k] > fitness[i] and age[k] < age[i]:
				onParetoFront = False
				#print(fitness[i], age[i], fitness[k], age[k])
		
		if onParetoFront:
			pareto_fitnesses[i] = 1

	return pareto_fitnesses

def GetParetoLevels(fitness, age):
	pareto_levels = np.zeros(len(fitness))

	for i in range(len(fitness)):

		for k in range(len(fitness)):
			if fitness[k] > fitness[i] and age[k] < age[i]:
				pareto_levels[i] += 1

	return pareto_levels

datapoints=np.random.rand(2, 50)
#print(datapoints)

paretoFront = GetParetoFront(datapoints[1,:], datapoints[0,:])
paretoLevels = GetParetoLevels(datapoints[1,:], datapoints[0,:])

for i in range(len(paretoLevels)):
	if paretoLevels[i] == 0:
		paretoLevels[i] = -5

plt.scatter(datapoints[0,:], datapoints[1,:], c=paretoFront, cmap='tab10')
plt.title('Fitness vs. Age')
plt.xlabel('Age')
plt.ylabel('Fitness')
plt.show()

plt.scatter(datapoints[0,:], datapoints[1,:], c=paretoLevels, cmap='tab10')
plt.title('Fitness vs. Age')
plt.xlabel('Age')
plt.ylabel('Fitness')
plt.show()