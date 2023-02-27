import os
from parallelHillClimber import PARALLEL_HILL_CLIMBER
from matplotlib import pyplot as plt
import constants as c
import numpy as np

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
plt.legend(['Population 1', 'Population 2', 'Population 3', 'Population 4', 'Population 5'], loc='upper left')
plt.show()