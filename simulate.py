import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
import numpy as np
import time

physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

planeId = p.loadURDF("plane.urdf")
robotId = p.loadURDF("body.urdf")

p.loadSDF("world.sdf")

# Set the gravity vector
p.setGravity(0,0,-9.8)

# Perform setup necessary to use sensors
pyrosim.Prepare_To_Simulate(robotId)

# Vectors to store front and back leg sensor values
frontLegSensorValues = np.zeros(100)
backLegSensorValues = np.zeros(100)

for i in range(100):
	p.stepSimulation()

	backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
	frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")

	print(i)
	time.sleep(1/60)

p.disconnect()

np.save('./data/frontLegSensorValues.npy', frontLegSensorValues)
np.save('./data/backLegSensorValues.npy', backLegSensorValues)