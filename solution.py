import pyrosim.pyrosim as pyrosim
import numpy as np
import random
import time
import os

class SOLUTION:

	def __init__(self, nextAvailableID):

		self.weights = np.random.rand(3,2)*2 - 1
		self.myID = nextAvailableID

	def Set_ID(self, id):
		self.myID = id
		
	def Start_Simulation(self, directOrGUI):
		self.Create_World()
		self.Create_Body()
		self.Create_Brain()
		os.system("python3 simulate.py " + directOrGUI + " " + str(self.myID) + " &")

	def Wait_For_Simulation_To_End(self):
		fitnessFileName = "fitness" + str(self.myID) + ".txt"
		while not os.path.exists(fitnessFileName):
			time.sleep(0.01)

		fitnessFile = open(fitnessFileName, "r")
		self.fitness = float(fitnessFile.read())
		os.system("rm fitness" + str(self.myID) + ".txt")

	def Mutate(self):
		randomRow = random.randint(0,2)
		randomColumn = random.randint(0,1)
		self.weights[randomRow,randomColumn] = random.random()*2 - 1

	def Create_World(self):
		length = 1
		width = 1
		height = 1

		x = 0
		y = 0
		z = height/2

		pyrosim.Start_SDF("world.sdf")

		pyrosim.Send_Cube(name="Box", pos=[-4,4,z] , size=[length,width,height])

		pyrosim.End()

	def Create_Body(self):
		length = 1
		width = 1
		height = 1

		pyrosim.Start_URDF("body.urdf")

		pyrosim.Send_Cube(name="Torso", pos=[1.5,0,1.5] , size=[length,width,height])
		pyrosim.Send_Joint( name = "Torso_BackLeg" , parent= "Torso" , child = "BackLeg" , type = "revolute", position = [1,0,1])
		pyrosim.Send_Cube(name="BackLeg", pos=[-0.5,0,-0.5] , size=[length,width,height])
		pyrosim.Send_Joint( name = "Torso_FrontLeg" , parent= "Torso" , child = "FrontLeg" , type = "revolute", position = [2,0,1])
		pyrosim.Send_Cube(name="FrontLeg", pos=[0.5,0,-0.5] , size=[length,width,height])


		pyrosim.End()

	def Create_Brain(self):
		pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")

		# Sensor neurons
		pyrosim.Send_Sensor_Neuron(name = 0 , linkName = "Torso")
		pyrosim.Send_Sensor_Neuron(name = 1 , linkName = "BackLeg")
		pyrosim.Send_Sensor_Neuron(name = 2 , linkName = "FrontLeg")

		# Motor neurons
		pyrosim.Send_Motor_Neuron( name = 3 , jointName = "Torso_BackLeg")
		pyrosim.Send_Motor_Neuron( name = 4 , jointName = "Torso_FrontLeg")

		for currentRow in range(3):
			for currentColumn in range(2):
				pyrosim.Send_Synapse( sourceNeuronName = currentRow , targetNeuronName = currentColumn+3 , weight = self.weights[currentRow][currentColumn] )

		pyrosim.End()