import random

class BODY:

	def __init__(self, parent, index, depth, totalDepth, jointPos, jointAxis):

		self.length = random.random() + 0.2
		self.width = random.random() + 0.2
		self.height = random.random() + 0.2
		self.hasSensor = random.random() > 0.5
		self.jointPos = jointPos
		self.jointAxis = jointAxis

		self.depth = depth
		self.parent = parent
		self.children = []
		self.nextAvailableIndex = index
		self.linksWithSensors = []
		self.numLinks = 0

		if depth > 1:
			if depth == totalDepth:
				numChildren = random.randint(1,4)
			else:
				numChildren = random.randint(0,1)

			jointPosOptions = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
			jointAxesOptions = ["1 0 0", "0 1 0", "0 0 1"]

			for i in range(numChildren):
				jointPos = random.choice(jointPosOptions)
				jointPosOptions.remove(jointPos)
				jointAxis = random.choice(jointAxesOptions)

				child = BODY(self, self.nextAvailableIndex, depth-1, totalDepth, jointPos, jointAxis)

				self.children.append(child)

				if child.hasSensor:
					self.linksWithSensors += [child.index]

		self.index = self.nextAvailableIndex

		if self.parent != None:
			self.parent.nextAvailableIndex = self.nextAvailableIndex+1
			self.parent.linksWithSensors += self.linksWithSensors
			self.parent.numLinks += len(self.children) + 1
		else:
			if self.hasSensor:
				self.linksWithSensors += [self.index]

			self.numLinks += 1


	def numNodes(self):
		return self.children.length

	def Print(self):
		print(f"Index", self.index, "has children:")
		for child in self.children:
			print(child.index, child.hasSensor)
		
		print("")

		for child in self.children:
			child.Print()

	def Get_rgba(self):
		if self.hasSensor == False:
			return "0 0 1.0 1.0"
		elif self.hasSensor == True:
			return "0 1.0 0 1.0"
		else:
			return "0 1.0 1.0 1.0"