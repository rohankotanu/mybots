from solution import SOLUTION
import pickle
import sys
import os

file_name = sys.argv[1]

best_solution = pickle.load( open("./solutions/" + file_name, "rb" ) )
best_solution.Start_Simulation("GUI")