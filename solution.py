import pyrosim.pyrosim as pyrosim
import constants as c
import numpy as np
import random
import time
import os

class SOLUTION:

	def __init__(self, nextAvailableID):

		self.weights = np.random.rand(c.numSensorNeurons,c.numMotorNeurons)*2 - 1
		self.myID = nextAvailableID

	def Set_ID(self, id):
		self.myID = id
		
	def Start_Simulation(self, directOrGUI):
		self.Create_World()
		self.Create_Body()
		self.Create_Brain()
		os.system("python3 simulate.py " + directOrGUI + " " + str(self.myID) + " 2&>1 &")
		#os.system("python3 simulate.py " + directOrGUI + " " + str(self.myID) + " &")

	def Wait_For_Simulation_To_End(self):
		fitnessFileName = "fitness" + str(self.myID) + ".txt"
		while not os.path.exists(fitnessFileName):
			time.sleep(0.01)

		fitnessFile = open(fitnessFileName, "r")
		self.fitness = float(fitnessFile.read())
		os.system("rm fitness" + str(self.myID) + ".txt")

	def Mutate(self):
		randomRow = random.randint(0,c.numSensorNeurons-1)
		randomColumn = random.randint(0,c.numMotorNeurons-1)
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
		palm_length = 1.2
		palm_width = 1.2
		palm_height = 0.2

		link1_length = 1
		link2_length = 0.5

		pyrosim.Start_URDF("body.urdf")


		# Hand
		pyrosim.Send_Cube(name="Palm", pos=[0,0,1] , size=[palm_length,palm_width,palm_height])


		# Upper Legs
		pyrosim.Send_Joint( name = "Palm_IndexLink1" , parent= "Palm" , child = "IndexLink1" , type = "revolute", position = [-palm_length/2,-0.45,1], jointAxis = "0 1 0")
		pyrosim.Send_Cube(name="IndexLink1", pos=[-0.5,0,0] , size=[link1_length,0.2,0.2])

		pyrosim.Send_Joint( name = "Palm_MiddleLink1" , parent= "Palm" , child = "MiddleLink1" , type = "revolute", position = [-palm_length/2,-0.15,1], jointAxis = "0 1 0")
		pyrosim.Send_Cube(name="MiddleLink1", pos=[-0.5,0,0] , size=[link1_length,0.2,0.2])

		pyrosim.Send_Joint( name = "Palm_RingLink1" , parent= "Palm" , child = "RingLink1" , type = "revolute", position = [-palm_length/2,0.15,1], jointAxis = "0 1 0")
		pyrosim.Send_Cube(name="RingLink1", pos=[-0.5,0,0] , size=[link1_length,0.2,0.2])

		pyrosim.Send_Joint( name = "Palm_PinkyLink1" , parent= "Palm" , child = "PinkyLink1" , type = "revolute", position = [-palm_length/2,0.45,1], jointAxis = "0 1 0")
		pyrosim.Send_Cube(name="PinkyLink1", pos=[-0.5,0,0] , size=[link1_length,0.2,0.2])

		pyrosim.Send_Joint( name = "Palm_ThumbLink1" , parent= "Palm" , child = "ThumbLink1" , type = "revolute", position = [0,-palm_length/2,1], jointAxis = "0.707 0.707 0")
		pyrosim.Send_Cube(name="ThumbLink1", pos=[0,-0.25,0] , size=[0.2,0.5,0.2])


		# Lower Legs
		pyrosim.Send_Joint( name = "IndexLink1_IndexLink2" , parent= "IndexLink1" , child = "IndexLink2" , type = "revolute", position = [-1,0,0], jointAxis = "0 1 0")
		pyrosim.Send_Cube(name="IndexLink2", pos=[0,0,-link2_length/2] , size=[0.2,0.2,link2_length])

		pyrosim.Send_Joint( name = "MiddleLink1_MiddleLink2" , parent= "MiddleLink1" , child = "MiddleLink2" , type = "revolute", position = [-1,0,0], jointAxis = "0 1 0")
		pyrosim.Send_Cube(name="MiddleLink2", pos=[0,0,-link2_length/2] , size=[0.2,0.2,link2_length])

		pyrosim.Send_Joint( name = "RingLink1_RingLink2" , parent= "RingLink1" , child = "RingLink2" , type = "revolute", position = [-1,0,0], jointAxis = "0 1 0")
		pyrosim.Send_Cube(name="RingLink2", pos=[0,0,-link2_length/2] , size=[0.2,0.2,link2_length])

		pyrosim.Send_Joint( name = "PinkyLink1_PinkyLink2" , parent= "PinkyLink1" , child = "PinkyLink2" , type = "revolute", position = [-1,0,0], jointAxis = "0 1 0")
		pyrosim.Send_Cube(name="PinkyLink2", pos=[0,0,-link2_length/2] , size=[0.2,0.2,link2_length])

		pyrosim.Send_Joint( name = "ThumbLink1_ThumbLink2" , parent= "ThumbLink1" , child = "ThumbLink2" , type = "revolute", position = [0,-0.5,0], jointAxis = "0 1 0")
		pyrosim.Send_Cube(name="ThumbLink2", pos=[0,0,-0.15] , size=[0.2,0.2,0.3])

		
		pyrosim.End()

	def Create_Brain(self):
		pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")

		# Sensor neurons
		pyrosim.Send_Sensor_Neuron(name = 0 , linkName = "Palm")

		pyrosim.Send_Sensor_Neuron(name = 1 , linkName = "IndexLink1")
		pyrosim.Send_Sensor_Neuron(name = 2 , linkName = "MiddleLink1")
		pyrosim.Send_Sensor_Neuron(name = 3 , linkName = "RingLink1")
		pyrosim.Send_Sensor_Neuron(name = 4 , linkName = "PinkyLink1")
		pyrosim.Send_Sensor_Neuron(name = 5 , linkName = "ThumbLink1")

		pyrosim.Send_Sensor_Neuron(name = 6 , linkName = "IndexLink2")
		pyrosim.Send_Sensor_Neuron(name = 7 , linkName = "MiddleLink2")
		pyrosim.Send_Sensor_Neuron(name = 8 , linkName = "RingLink2")
		pyrosim.Send_Sensor_Neuron(name = 9 , linkName = "PinkyLink2")
		pyrosim.Send_Sensor_Neuron(name = 10 , linkName = "ThumbLink2")


		# Motor neurons
		pyrosim.Send_Motor_Neuron( name = 11 , jointName = "Palm_IndexLink1")
		pyrosim.Send_Motor_Neuron( name = 12 , jointName = "Palm_MiddleLink1")
		pyrosim.Send_Motor_Neuron( name = 13 , jointName = "Palm_RingLink1")
		pyrosim.Send_Motor_Neuron( name = 14 , jointName = "Palm_PinkyLink1")
		pyrosim.Send_Motor_Neuron( name = 15 , jointName = "Palm_ThumbLink1")

		pyrosim.Send_Motor_Neuron( name = 16 , jointName = "IndexLink1_IndexLink2")
		pyrosim.Send_Motor_Neuron( name = 17 , jointName = "MiddleLink1_MiddleLink2")
		pyrosim.Send_Motor_Neuron( name = 18 , jointName = "RingLink1_RingLink2")
		pyrosim.Send_Motor_Neuron( name = 19 , jointName = "PinkyLink1_PinkyLink2")
		pyrosim.Send_Motor_Neuron( name = 20 , jointName = "ThumbLink1_ThumbLink2")


		for currentRow in range(c.numSensorNeurons):
			for currentColumn in range(c.numMotorNeurons):
				pyrosim.Send_Synapse( sourceNeuronName = currentRow , targetNeuronName = currentColumn+c.numSensorNeurons , weight = self.weights[currentRow][currentColumn] )

		pyrosim.End()