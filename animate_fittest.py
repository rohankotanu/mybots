from solution import SOLUTION
import pickle

best_solution = pickle.load( open( "fittest.p", "rb" ) )
best_solution.Start_Simulation("GUI")