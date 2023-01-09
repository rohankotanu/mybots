import pyrosim.pyrosim as pyrosim

length = 1
width = 1
height = 1

x = 0
y = 0
z = height/2

pyrosim.Start_SDF("boxes.sdf")

for i in range(5):
	for j in range(5):
		for k in range(10):
			pyrosim.Send_Cube(name="Box", pos=[-2+i,-2+j,z+k] , size=[length*0.9**k,width*0.9**k,height*0.9**k])


pyrosim.End()