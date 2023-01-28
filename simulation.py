import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
from world import WORLD
from robot import ROBOT
import time

class SIMULATION:

	def __init__(self, directOrGUI, solutionID):

		# Connect to pybullet
		if directOrGUI == "DIRECT":
			self.physicsClient = p.connect(p.DIRECT)
		else:
			self.physicsClient = p.connect(p.GUI)

		# Set additional search path
		p.setAdditionalSearchPath(pybullet_data.getDataPath())

		# Set the gravity vector
		p.setGravity(0,0,-9.8)

		self.world = WORLD()
		self.robot = ROBOT(solutionID)



	def Run(self):
		for t in range(1000):
			p.stepSimulation()
			self.robot.Sense(t)
			self.robot.Think()
			self.robot.Act(t)


			#print(t)
			time.sleep(1/1000)


	def Get_Fitness(self):
		self.robot.Get_Fitness()

	def __del__(self):

		p.disconnect()