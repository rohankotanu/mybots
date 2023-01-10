import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
import numpy as np
import random
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
frontLegSensorValues = np.zeros(1000)
backLegSensorValues = np.zeros(1000)

x = np.linspace(0, 2*np.pi, 1000)

# Parameters for front leg motion
amplitude = np.pi/4
frequency = 10
phaseOffset = 0

# Vector of front leg angles
frontLegTargetAngles = amplitude*np.sin(frequency*x + phaseOffset)
# np.save('./data/frontLegTargetAngles.npy', frontLegTargetAngles)

# Parameters for back leg motion
amplitude = np.pi/4
frequency = 1
phaseOffset = np.pi/4

# Vector of back leg angles
backLegTargetAngles = amplitude*np.sin(frequency*x + phaseOffset)
# np.save('./data/backLegTargetAngles.npy', backLegTargetAngles)
# exit()



for i in range(1000):
	p.stepSimulation()

	backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
	frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")

	pyrosim.Set_Motor_For_Joint(

		bodyIndex = robotId,

		jointName = b'Torso_FrontLeg',

		controlMode = p.POSITION_CONTROL,

		targetPosition = frontLegTargetAngles[i],

		maxForce = 100)

	pyrosim.Set_Motor_For_Joint(

		bodyIndex = robotId,

		jointName = b'Torso_BackLeg',

		controlMode = p.POSITION_CONTROL,

		targetPosition = backLegTargetAngles[i],

		maxForce = 100)

	print(i)
	time.sleep(1/240)

p.disconnect()

np.save('./data/frontLegSensorValues.npy', frontLegSensorValues)
np.save('./data/backLegSensorValues.npy', backLegSensorValues)