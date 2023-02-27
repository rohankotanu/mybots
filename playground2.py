import pyrosim.pyrosim as pyrosim
from body import BODY
import pybullet as p
import pybullet_data
import random
import time

depth = 3

root = BODY(None, 0, depth, depth, None, None)

for i in range(100):
	
	root.Print()
	print(root.linksBelow)

	print('------------------')

	root.Mutate()


	root.Print()
	print(root.linksBelow)

	print('------------------')

	root.Mutate()


	root.Print()
	print(root.linksBelow)
