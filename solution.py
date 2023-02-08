import pyrosim.pyrosim as pyrosim
import constants as c
import numpy as np
import random
import time
import os

class SOLUTION:

	def __init__(self, nextAvailableID, populationID):

		self.myID = nextAvailableID
		self.populationID = populationID
		self.Create_Body()

	def Set_ID(self, id):
		self.myID = id
		
	def Start_Simulation(self, directOrGUI):
		self.Create_World()
		self.Create_Brain()
		os.system("python3 simulate.py " + directOrGUI + " " + str(self.myID) + " " + str(self.populationID) + " 2&>1 &")
		#os.system("python3 simulate.py " + directOrGUI + " " + str(self.myID) + " " + str(self.populationID) + " &")

	def Wait_For_Simulation_To_End(self):
		fitnessFileName = "fitness" + str(self.myID) + ".txt"
		while not os.path.exists(fitnessFileName):
			time.sleep(0.01)

		fitnessFile = open(fitnessFileName, "r")
		self.fitness = float(fitnessFile.read())
		os.system("rm fitness" + str(self.myID) + ".txt")

	def Mutate(self):
		randomRow = random.randint(0,self.numSensorNeurons-1)
		randomColumn = random.randint(0,self.numLinks-2)
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
		head_length = random.random() + 0.2
		head_width = random.random() + 0.2
		head_height = random.random() + 0.2


		pyrosim.Start_URDF("body" + str(self.populationID) + ".urdf")


		# Length of body
		self.numLinks = random.randint(3,10)
		self.sensorLocs = np.random.randint(2, size=self.numLinks)

		material = "Green" if self.sensorLocs[0] == 1 else "Blue"

		# Head
		pyrosim.Send_Cube(name="Link1", pos=[0,0,1] , size=[head_length,head_width,head_height], material = material, rgba = self.Get_rgba(material))


		# Link 1
		link_length = random.random() + 0.2
		link_width = random.random() + 0.2
		link_height = random.random() + 0.2
		material = "Green" if self.sensorLocs[1] == 1 else "Blue"
		pyrosim.Send_Joint( name = "Link1_Link2" , parent= "Link1" , child = "Link2" , type = "revolute", position = [head_length/2,0,1], jointAxis = "0 1 0")
		pyrosim.Send_Cube(name= "Link2", pos=[link_length/2,0,0] , size=[link_length,link_width,link_height], material = material, rgba = self.Get_rgba(material))


		prevLinkLength = link_length


		# Additional links
		for i in range(2,self.numLinks):
			link_length = random.random() + 0.2
			link_width = random.random() + 0.2
			link_height = random.random() + 0.2

			jointName = "Link" + str(i) + "_Link" + str(i+1)
			parentName = "Link" + str(i)
			childName = "Link" + str(i+1)

			pyrosim.Send_Joint( name = jointName , parent= parentName , child = childName , type = "revolute", position = [prevLinkLength,0,0], jointAxis = "0 1 0")
			material = "Green" if self.sensorLocs[i] == 1 else "Blue"
			pyrosim.Send_Cube(name= childName, pos=[link_length/2,0,0] , size=[link_length,link_width,link_height], material = material, rgba = self.Get_rgba(material))

			prevLinkLength = link_length

		
		pyrosim.End()

	def Create_Brain(self):
		pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")

		neuronName = 0

		for i in range(self.numLinks):

			if self.sensorLocs[i] == 1:
				linkName = "Link" + str(i+1)
				pyrosim.Send_Sensor_Neuron(name = neuronName , linkName = linkName)

				neuronName += 1


		self.numSensorNeurons = neuronName


		# Motor neurons
		for i in range(1,self.numLinks):
			jointName = "Link" + str(i) + "_Link" + str(i+1)
			pyrosim.Send_Motor_Neuron( name = neuronName , jointName = jointName)

			neuronName += 1


		self.weights = np.random.rand(self.numSensorNeurons, self.numLinks-1)*2 - 1


		for currentRow in range(self.numSensorNeurons):
			for currentColumn in range(self.numLinks-1):
				pyrosim.Send_Synapse( sourceNeuronName = currentRow , targetNeuronName = currentColumn+self.numSensorNeurons , weight = self.weights[currentRow][currentColumn] )

		pyrosim.End()


	def Get_rgba(self, material):
		if material == "Blue":
			return "0 0 1.0 1.0"
		elif material == "Green":
			return "0 1.0 0 1.0"
		else:
			return "0 1.0 1.0 1.0"
