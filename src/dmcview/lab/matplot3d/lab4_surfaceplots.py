import numpy as np
import matplotlib.pyplot as plt

def function_z(x, y):
    return 50 -(x**2 + y**2)


space = 10

x_values = np.linspace(-5, 5, space)
y_values = np.linspace(-5, 5, space)

X, Y = np.meshgrid(x_values,y_values)

#plt.scatter(X,Y)
#plt.show()

Z = function_z(X, Y)

ax = plt.axes(projection='3d')
#ax.plot_surface(X,Y,Z)
ax.plot_wireframe(X,Y,Z, color="black")

plt.show()