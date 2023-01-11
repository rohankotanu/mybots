import pybullet as p
import pyrosim.pyrosim as pyrosim
import numpy as np
import constants as c

class MOTOR:

	def __init__(self,jointName):

		self.jointName = jointName
		self.Prepare_To_Act()


	def Prepare_To_Act(self):
		self.amplitude = c.amplitude
		self.frequency = c.frequency
		self.offset = c.phaseOffset

		if(self.jointName == b'Torso_BackLeg'):
			self.frequency = self.frequency/2

		# Vector of motor angles
		x = np.linspace(0, 2*np.pi, 1000)
		self.motorValues = self.amplitude*np.sin(self.frequency*x + self.offset)


	def Set_Value(self,robotId,t):
		pyrosim.Set_Motor_For_Joint(

			bodyIndex = robotId,

			jointName = self.jointName,

			controlMode = p.POSITION_CONTROL,

			targetPosition = self.motorValues[t],

			maxForce = 300)


	def Save_Values(self):
		destinationPath = "./data/" + self.jointName + "TargetAngles.npy"
		np.save(destinationPath, self.values)

