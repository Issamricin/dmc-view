import matplotlib.pyplot as plt
import numpy as np

ax = plt.axes(projection = "3d")

x_data = np.random.randint(0,100,555)
y_data = np.random.randint(0,100,555)
z_data = np.random.randint(0,100,555)

ax.scatter(x_data,y_data,z_data,marker="v")

plt.show()