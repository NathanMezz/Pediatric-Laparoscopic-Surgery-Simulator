from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt

fig = plt.figure()
ax = plt.axes(projection="3d")

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

x_arr = np.array(range(0, 100))
y_arr = np.array(range(0, 100))
z_arr = np.array(range(0, 100))

ax.plot3D(x_arr,y_arr,z_arr, 'blue')

ax.scatter3D(x_arr, y_arr, z_arr, c ='red');
plt.show()