import pyrosim.pyrosim as pyrosim
import numpy as np

class SENSOR:

	def __init__(self,linkName):

		self.linkName = linkName
		self.values = np.zeros(1000)


	def Get_Value(self,t):
		self.values[t] = pyrosim.Get_Touch_Sensor_Value_For_Link(self.linkName)


	def Save_Values(self):
		destinationPath = "./data/" + self.linkName + "SensorValues.npy"
		np.save(destinationPath, self.values)