import numpy as np
import constants as c
from simulation import SIMULATION
import random
import sys

directOrGUI = sys.argv[1]
solutionID = sys.argv[2]
populationID = sys.argv[3]


simulation = SIMULATION(directOrGUI, solutionID, populationID)
simulation.Run()
simulation.Get_Fitness()