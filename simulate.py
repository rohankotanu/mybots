import numpy as np
import constants as c
from simulation import SIMULATION
import random
import sys

directOrGUI = sys.argv[1]


simulation = SIMULATION(directOrGUI)
simulation.Run()
simulation.Get_Fitness()