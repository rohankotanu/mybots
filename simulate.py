import pybullet as p
import pybullet_data
import time

physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

planeId = p.loadURDF("plane.urdf")
robotId = p.loadURDF("body.urdf")

p.loadSDF("world.sdf")

p.setGravity(0,0,-9.8)

for i in range(1000):
	p.stepSimulation()
	print(i)
	time.sleep(1/60)

p.disconnect()