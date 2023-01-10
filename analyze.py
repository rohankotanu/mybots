import numpy as np
import matplotlib.pyplot as plt

frontLegSensorValues = np.load('./data/frontLegSensorValues.npy')
backLegSensorValues = np.load('./data/backLegSensorValues.npy')
frontLegTargetAngles = np.load('./data/frontLegTargetAngles.npy')
backLegTargetAngles = np.load('./data/backLegTargetAngles.npy')

plt.plot(backLegTargetAngles,label='backLeg Target Angles',linewidth=4)
plt.plot(frontLegTargetAngles,label='frontLeg Target Angles')
# plt.plot(frontLegSensorValues,label='Front Leg',linewidth=4)
# plt.plot(backLegSensorValues,label='Back Leg')

plt.legend()
plt.show()