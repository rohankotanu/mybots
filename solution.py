import pyrosim.pyrosim as pyrosim
from body import BODY
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
		randomColumn = random.randint(0,self.root.numLinks-2)
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

		depth = random.randint(2,4)
		self.root = BODY(None, 0, depth, depth, None, None)

		head_length = self.root.length
		head_width = self.root.width
		head_height = self.root.height
		material = "Green" if self.root.hasSensor == True else "Blue"
		startingHeight = 2

		rootLinkName = "Link" + str(self.root.index)

		# Body
		pyrosim.Send_Cube(name=rootLinkName, pos=[0,0,startingHeight] , size=[head_length,head_width,head_height], material = material, rgba = self.root.Get_rgba())

		self.attachChildren(self.root, depth, startingHeight, head_length, head_width, head_height)

		pyrosim.End()

	def Create_Brain(self):
		pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")

		neuronName = 100

		for i in range(self.root.numLinks):

			if i in self.root.linksWithSensors:
				linkName = "Link" + str(i)
				pyrosim.Send_Sensor_Neuron(name = neuronName , linkName = linkName)

				neuronName += 1


		self.numSensorNeurons = len(self.root.linksWithSensors)

		# Motor neurons
		self.attachMotorNeuron(self.root)


		self.weights = np.random.rand(self.numSensorNeurons, self.root.numLinks-1)*2 - 1


		for currentRow in range(self.numSensorNeurons):
			for currentColumn in range(self.root.numLinks-1):
				pyrosim.Send_Synapse( sourceNeuronName = 100+currentRow , targetNeuronName = currentColumn , weight = self.weights[currentRow][currentColumn] )

		pyrosim.End()


	def attachChildren(self, parent, totalDepth, startingHeight, head_length, head_width, head_height):

		# Child Links
		for i in range(len(parent.children)):
			child = parent.children[i]

			link_length = child.length
			link_width = child.width
			link_height = child.height

			material = "Green" if child.hasSensor == True else "Blue"

			if parent.depth == totalDepth:

				parentLinkName = "Link" + str(parent.index)
				jointName = "Link" + str(parent.index) + "_Link" + str(child.index)
				linkName = "Link" + str(child.index)

				posID = child.jointPos
				jointAxis = child.jointAxis

				if posID == 0:
					jointPosition = [head_length/2,head_width/2,startingHeight]
					linkPosition = [link_length/2,link_width/2,0]
				elif posID == 1:
					jointPosition = [-head_length/2,head_width/2,startingHeight]
					linkPosition = [-link_length/2,link_width/2,0]
				elif posID == 2:
					jointPosition = [-head_length/2,-head_width/2,startingHeight]
					linkPosition = [-link_length/2,-link_width/2,0]
				elif posID == 3:
					jointPosition = [head_length/2,-head_width/2,startingHeight]
					linkPosition = [link_length/2,-link_width/2,0]
				elif posID == 4:
					jointPosition = [head_length/2,0,head_height/2+startingHeight]
					linkPosition = [link_length/2,0,link_height/2]
				elif posID == 5:
					jointPosition = [0,head_width/2,head_height/2+startingHeight]
					linkPosition = [0,link_width/2,link_height/2]
				elif posID == 6:
					jointPosition = [-head_length/2,0,head_height/2+startingHeight]
					linkPosition = [-link_length/2,0,link_height/2]
				elif posID == 7:
					jointPosition = [0,-head_width/2,head_height/2+startingHeight]
					linkPosition = [0,-link_width/2,link_height/2]
				elif posID == 8:
					jointPosition = [head_length/2,0,-head_height/2+startingHeight]
					linkPosition = [link_length/2,0,-link_height/2]
				elif posID == 9:
					jointPosition = [0,head_width/2,-head_height/2+startingHeight]
					linkPosition = [0,link_width/2,-link_height/2]
				elif posID == 10:
					jointPosition = [-head_length/2,0,-head_height/2+startingHeight]
					linkPosition = [-link_length/2,0,-link_height/2]
				elif posID == 11:
					jointPosition = [0,-head_width/2,-head_height/2+startingHeight]
					linkPosition = [0,-link_width/2,-link_height/2]

				
				pyrosim.Send_Joint( name = jointName , parent= parentLinkName , child = linkName , type = "revolute", position = jointPosition, jointAxis = jointAxis)
				pyrosim.Send_Cube(name= linkName, pos=linkPosition, size=[link_length,link_width,link_height], material = material, rgba = child.Get_rgba())

			else:
				parentLinkName = "Link" + str(parent.index)
				jointName = "Link" + str(parent.index) + "_Link" + str(child.index)
				linkName = "Link" + str(child.index)

				parentPos = parent.jointPos

				if parentPos >= 4 and parentPos <= 7:
					jointPosition = [0,0,parent.height]
					linkPosition = [0,0,link_height/2]
				elif parentPos == 0 or parentPos == 3:
					jointPosition = [parent.length,0,0]
					linkPosition = [link_length/2,0,0]
				elif parentPos == 1 or parentPos == 2:
					jointPosition = [-parent.length,0,0]
					linkPosition = [-link_length/2,0,0]
				elif parentPos >= 8:
					jointPosition = [0,0,-parent.height]
					linkPosition = [0,0,-link_height/2]

				pyrosim.Send_Joint( name = jointName , parent= parentLinkName , child = linkName , type = "revolute", position = jointPosition, jointAxis = child.jointAxis)
				pyrosim.Send_Cube(name= linkName, pos=linkPosition, size=[link_length,link_width,link_height], material = material, rgba = child.Get_rgba())


			self.attachChildren(child, totalDepth, startingHeight, head_length, head_width, head_height)


	def attachMotorNeuron(self, parent):

		# Child Links
		for i in range(len(parent.children)):
			child = parent.children[i]

			jointName = "Link" + str(parent.index) + "_Link" + str(child.index)
			neuronName = child.index
			
			pyrosim.Send_Motor_Neuron(name = neuronName , jointName = jointName)

			self.attachMotorNeuron(child)
