from solution import SOLUTION
import pickle
import os

best_solution = pickle.load( open( "fittest.p", "rb" ) )
best_solution.Start_Simulation("GUI")