from link import LINK
import random

#depth = random.randint(1,3)
depth = 3
print("Depth: ", depth)

root = LINK(None, 0, depth, depth, None, None)

root.Print()

print(root.linksWithSensors)
print(root.numLinks)