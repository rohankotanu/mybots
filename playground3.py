import pyrosim.pyrosim as pyrosim
from body import BODY
import pybullet as p
import pybullet_data
import random
import time


def attachChildren(parent, totalDepth, startingHeight):

	# Child Links
	for i in range(len(parent.children)):
		child = parent.children[i]

		link_length = child.length
		link_width = child.width
		link_height = child.height

		material = "Green" if child.hasSensor == True else "Blue"

		if parent.depth == totalDepth:

			jointName = "Head_Link" + str(child.index)
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

			
			pyrosim.Send_Joint( name = jointName , parent= "Head" , child = linkName , type = "revolute", position = jointPosition, jointAxis = jointAxis)
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


		attachChildren(child, totalDepth, startingHeight)



depth = random.randint(1,4)
print("Depth: ", depth)

root = BODY(None, 0, depth, depth, None, None)

root.Print()


pyrosim.Start_URDF("test_body.urdf")

head_length = root.length
head_width = root.width
head_height = root.height
material = "Green" if root.hasSensor == True else "Blue"
startingHeight = 2

# Head
pyrosim.Send_Cube(name="Head", pos=[0,0,startingHeight] , size=[head_length,head_width,head_height], material = material, rgba = root.Get_rgba())

attachChildren(root, depth, startingHeight)

pyrosim.End()


physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

planeId = p.loadURDF("plane.urdf")

p.setGravity(0,0,-9.8)

p.loadURDF("test_body.urdf")

for i in range(1000):
	p.stepSimulation()
	print(i)
	time.sleep(1/100)

p.disconnect()