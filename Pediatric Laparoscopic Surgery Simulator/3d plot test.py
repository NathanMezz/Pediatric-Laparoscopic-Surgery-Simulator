from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt

fig = plt.figure()
ax = plt.axes(projection="3d")

x_arr = np.array(range(0, 100))
y_arr = np.array(range(0, 100))
z_arr = np.array(range(0, 100))

ax.plot3D(x_arr,y_arr,z_arr, 'blue')

plt.show()