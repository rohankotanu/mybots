import pybullet as p
import pyrosim.pyrosim as pyrosim
from pyrosim.neuralNetwork import NEURAL_NETWORK
from sensor import SENSOR
from motor import MOTOR
import os

class ROBOT:

	def __init__(self, solutionID):

		self.robotId = p.loadURDF("body.urdf")
		self.nn = NEURAL_NETWORK("brain" + solutionID + ".nndf")
		self.solutionID = solutionID

		# Perform setup necessary to use sensors
		pyrosim.Prepare_To_Simulate(self.robotId)

		self.Prepare_to_Sense()
		self.Prepare_to_Act()

		os.system("rm brain" + solutionID + ".nndf")


	def Prepare_to_Sense(self):
		self.sensors = {}
		
		for linkName in pyrosim.linkNamesToIndices:
			self.sensors[linkName] = SENSOR(linkName)


	def Sense(self,t):
		for linkName in self.sensors:
			self.sensors[linkName].Get_Value(t)


	def Prepare_to_Act(self):
		self.motors = {}
		
		for jointName in pyrosim.jointNamesToIndices:
			self.motors[jointName] = MOTOR(jointName)


	def Act(self,t):
		for neuronName in self.nn.Get_Neuron_Names():
			if self.nn.Is_Motor_Neuron(neuronName):
				jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)
				desiredAngle = self.nn.Get_Value_Of(neuronName)

				self.motors[bytes(jointName, 'utf-8')].Set_Value(self.robotId,desiredAngle)


	def Think(self):
		self.nn.Update()
		#self.nn.Print()

	def Get_Fitness(self):
		stateOfLinkZero = p.getLinkState(self.robotId, 0)
		positionOfLinkZero = stateOfLinkZero[0]
		xCoordinateOfLinkZero = positionOfLinkZero[0]

		f = open("tmp" + self.solutionID + ".txt", "w")
		f.write(str(xCoordinateOfLinkZero))
		f.close()

		os.system("mv tmp" + self.solutionID + ".txt fitness" + self.solutionID + ".txt")