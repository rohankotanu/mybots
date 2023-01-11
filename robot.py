import pybullet as p
import pyrosim.pyrosim as pyrosim
from sensor import SENSOR
from motor import MOTOR

class ROBOT:

	def __init__(self):

		self.robotId = p.loadURDF("body.urdf")

		# Perform setup necessary to use sensors
		pyrosim.Prepare_To_Simulate(self.robotId)

		self.Prepare_to_Sense()
		self.Prepare_to_Act()


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
		for jointName in self.motors:
			self.motors[jointName].Set_Value(self.robotId,t)