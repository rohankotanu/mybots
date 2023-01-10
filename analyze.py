import numpy as np
import matplotlib.pyplot as plt

frontLegSensorValues = np.load('./data/frontLegSensorValues.npy')
backLegSensorValues = np.load('./data/backLegSensorValues.npy')

plt.plot(frontLegSensorValues,label='Front Leg',linewidth=4)
plt.plot(backLegSensorValues,label='Back Leg')

plt.legend()
plt.show()