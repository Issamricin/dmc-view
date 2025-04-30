import numpy as np
import matplotlib.pyplot as plt


ax = plt.axes(projection="3d")

ax.set_xlim([-15, 15])
ax.set_ylim([-15, 15])
ax.set_zlim([-15, 15])
accel = np.array([12,12,0])
origin= np.array([0,0,0])

ax.quiver(*origin, *accel, color="Red", linewidth=2, arrow_length_ratio=0.3)

plt.show()