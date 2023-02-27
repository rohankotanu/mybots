import pyrosim.pyrosim as pyrosim
from body import BODY
import constants as c
import numpy as np
import random
import time
import os

class SOLUTION:

	def __init__(self, nextAvailableID):

		self.myID = nextAvailableID

		depth = random.randint(2,5)
		self.root = BODY(None, 0, depth, depth, None, None)
		

	def Set_ID(self, id):
		self.myID = id
		
	def Start_Simulation(self, directOrGUI):
		self.Create_World()
		self.Create_Body()
		self.Create_Brain()
		os.system("python3 simulate.py " + directOrGUI + " " + str(self.myID) + " 2&>1 &")
		#os.system("python3 simulate.py " + directOrGUI + " " + str(self.myID)  + " &")

	def Wait_For_Simulation_To_End(self):
		fitnessFileName = "fitness" + str(self.myID) + ".txt"
		while not os.path.exists(fitnessFileName):
			time.sleep(0.01)

		fitnessFile = open(fitnessFileName, "r")
		self.fitness = float(fitnessFile.read())
		os.system("rm fitness" + str(self.myID) + ".txt")

	def Mutate(self):
		self.root.Mutate()

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


		pyrosim.Start_URDF("body" + str(self.myID) + ".urdf")

		head_length = self.root.length
		head_width = self.root.width
		head_height = self.root.height
		material = "Green" if self.root.hasSensor == True else "Blue"
		startingHeight = 2

		rootLinkName = "Link" + str(self.root.index)

		# Body
		pyrosim.Send_Cube(name=rootLinkName, pos=[0,0,startingHeight] , size=[head_length,head_width,head_height], material = material, rgba = self.root.Get_rgba())

		self.attachChildren(self.root, self.root.depth, startingHeight, head_length, head_width, head_height)

		pyrosim.End()

	def Create_Brain(self):
		pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")


		for i in self.root.linksWithSensors:
			linkName = "Link" + str(i)
			pyrosim.Send_Sensor_Neuron(name = i+100 , linkName = linkName)


		self.numSensorNeurons = len(self.root.linksWithSensors)

		# Motor neurons
		self.attachMotorNeurons(self.root)

		# Attach synapses
		self.attachSynapses(self.root)

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


	def attachMotorNeurons(self, parent):

		# Child Links
		for i in range(len(parent.children)):
			child = parent.children[i]

			jointName = "Link" + str(parent.index) + "_Link" + str(child.index)
			neuronName = child.index
			
			pyrosim.Send_Motor_Neuron(name = neuronName , jointName = jointName)

			self.attachMotorNeurons(child)


	def attachSynapses(self, parent):

		# Child Links
		for child in parent.children:

			for index in child.linksWithSensors:
				pyrosim.Send_Synapse( sourceNeuronName = index+100 , targetNeuronName = child.index , weight = child.linksWithSensors[index] )


			self.attachSynapses(child)
