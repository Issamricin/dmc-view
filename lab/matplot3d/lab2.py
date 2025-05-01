import matplotlib.pyplot as plt
import numpy as np

ax = plt.axes(projection="3d")

x_data = np.arange(0,50,0.1)
y_data = np.arange(0,50,0.1)
z_data = np.sin(x_data) * np.cos(y_data)

ax.plot(x_data,y_data,z_data)

ax.set_title("Lab Function")
ax.set_ylabel("My Function (cm)")
ax.set_xlabel("My Function (cm)")
ax.set_zlabel("My Result (cm2)")

plt.show()