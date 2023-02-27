import random
import copy

class BODY:

	def __init__(self, parent, index, depth, totalDepth, jointPos, jointAxis):

		self.length = random.random() + 0.2
		self.width = random.random() + 0.2
		self.height = random.random() + 0.2
		self.hasSensor = random.random() > 0.5
		self.jointPos = jointPos
		self.jointAxis = jointAxis

		self.depth = depth
		self.totalDepth = totalDepth
		self.parent = parent
		self.children = []
		self.nextAvailableIndex = index
		self.linksBelow = []
		self.linksWithSensors = {}


		# If it's not the bottom-most level of the tree
		if depth > 1:
			# Between 1 and 4 childred for the root node
			if depth == totalDepth:
				numChildren = random.randint(1,4)
			# 0 or 1 children for all other nodes
			else:
				numChildren = random.randint(0,1)

			jointPosOptions = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
			jointAxesOptions = ["1 0 0", "0 1 0", "0 0 1"]

			for i in range(numChildren):
				jointPos = random.choice(jointPosOptions)
				jointPosOptions.remove(jointPos)
				jointAxis = random.choice(jointAxesOptions)

				# Create child node
				child = BODY(self, self.nextAvailableIndex, depth-1, totalDepth, jointPos, jointAxis)
				self.children.append(child)

		# Set index of self
		self.index = self.nextAvailableIndex

		# Add self to linksWithSensors if self has a sensor
		if self.hasSensor:
			self.linksWithSensors[self.index] = random.random()*2 - 1

		# Add self's index to linksBelow
		self.linksBelow += [self.index]

		# If not the root node
		if self.parent != None:
			# Increment the nextAvailableIndex of parent
			self.parent.nextAvailableIndex = self.nextAvailableIndex+1
			self.parent.linksBelow += self.linksBelow

			for index in self.linksWithSensors:
				self.parent.linksWithSensors[index] = random.random()*2 - 1




	def numNodes(self):
		return self.children.length

	def Print(self):
		print(f"Index", self.index, "has children:")
		for child in self.children:
			print(child.index, child.hasSensor)
		print(self.linksWithSensors)
		
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



	def Mutate(self):
		# Remove a link with probability 0.1
		if self.depth != self.totalDepth and random.random() < 0.01:
			#print("trying to remove", self.index)
			self.Remove(copy.deepcopy(self.linksBelow))
			
			if self.parent != None:
				self.parent.children.remove(self)
		else:
			# Add a link with probability 0.1
			if random.random() < 0.1:
				if (self.depth == self.totalDepth and len(self.children) < 4) or len(self.children) == 0:
					jointPosOptions = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
					jointAxesOptions = ["1 0 0", "0 1 0", "0 0 1"]

					jointPos = random.choice(jointPosOptions)
					jointAxis = random.choice(jointAxesOptions)

					index = random.randint(1000,10000)

					# Create child node
					child = BODY(self, index, 1, self.totalDepth, jointPos, jointAxis)
					self.children.append(child)

					self.Add(child, True)
				pass


			# Change length of cube with probability 0.3
			if random.random() < 0.3:
				self.length = random.random() + 0.2

			# Change width of cube with probability 0.3
			if random.random() < 0.3:
				self.width = random.random() + 0.2

			# Change height of cube with probability 0.3
			if random.random() < 0.3:
				self.height = random.random() + 0.2


			# Change joint axis with probability 0.2
			if random.random() < 0.2:
				jointAxesOptions = ["1 0 0", "0 1 0", "0 0 1"]
				jointAxis = random.choice(jointAxesOptions)
				self.jointAxis = jointAxis


			# Add sensor with probability 0.2
			if random.random() < 0.2:
				self.hasSensor = True
				self.AddSensor(self.index)

			# Remove sensor with probability 0.2
			if random.random() < 0.2:
				self.hasSensor = False
				self.RemoveSensor(self.index)


			# Alter weights with probability 0.1
			for key in self.linksWithSensors:
				if random.random() < 0.1:
					self.linksWithSensors[key] = random.random()*2 - 1


			for child in self.children:
				child.Mutate()


	def Remove(self, linksToRemove):
		for link in linksToRemove:
			self.linksWithSensors.pop(link, None)
			try:
				self.linksBelow.remove(link)
			except:
				pass

		if self.parent != None:
			self.parent.Remove(linksToRemove)

	def Add(self, newLink, directParentOfNewLink):
		if not directParentOfNewLink:
			self.linksBelow += [newLink.index]

			if newLink.hasSensor:
				self.linksWithSensors[newLink.index] = random.random()*2 - 1

		if self.parent != None:
			self.parent.Add(newLink, False)

	def AddSensor(self, index):
		self.linksWithSensors[index] = random.random()*2 - 1

		if self.parent != None:
			self.parent.AddSensor(index)

	def RemoveSensor(self, index):
		self.linksWithSensors.pop(index, None)

		if self.parent != None:
			self.parent.RemoveSensor(index)