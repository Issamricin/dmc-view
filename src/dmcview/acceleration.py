from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
from PySide6.QtCore import QTimer


class Accelaration_3D(FigureCanvas):
    def __init__(self, figure=None):
        super().__init__(figure)

        self.target_x = 0.0
        self.target_y = 0.0
        self.target_z = 0.0

        self.x = 0.0
        self.y = 0.0
        self.z = 0.0

        self.value = 0.2 #0.1 step is very slow

        last_x_digit = self.x*10
        last_x_digit = last_x_digit %10

        if last_x_digit % 2 != 0:
            self.x += 0.1  #since the step is 0.2 we will make odd inputs into even.

        last_y_digit = self.y*10
        last_y_digit = last_y_digit %10

        if last_y_digit % 2 != 0:
            self.y += 0.1  #since the step is 0.2 we will make odd inputs into even.

        last_z_digit = self.z*10
        last_z_digit = last_z_digit %10

        if last_z_digit % 2 != 0:
            self.z += 0.1  #since the step is 0.2 we will make odd inputs into even.
            
        self.figure = Figure()
        self.ax = self.figure.add_subplot(projection='3d')

        self.ax.set_xlim([-15, 15])
        self.ax.set_ylim([-15, 15])
        self.ax.set_zlim([-15, 15])
        self.ax.set_title("3D Acceleration")

        self.quiver = self.ax.quiver(0, 0, 0, 0, 0, 0, color="red", linewidth=2, arrow_length_ratio=0.3)

        self.ax.view_init(azim=-115,elev=20,roll=3)
        self.start_acceleration_timer()


    def update_acceleration_vector(self) -> None:

        self.target_x = round(self.target_x,1)
        self.target_y = round(self.target_y,1)
        self.target_z = round(self.target_z,1)

        if self.target_x < self.x:
            self.target_x += self.value
        elif self.target_x > self.x:
            self.target_x -= self.value

        if self.target_y < self.y:
            self.target_y += self.value
        elif self.target_y > self.y:
            self.target_y -= self.value

        if self.target_z < self.z:
            self.target_z += self.value
        elif self.target_z > self.z:
            self.target_z -= self.value

        accel = np.array([self.target_x,self.target_y,self.target_z])
        origin= np.array([0,0,0])

        self.quiver.remove()
        self.quiver = self.ax.quiver(*origin, *accel, color="Red", linewidth=2, arrow_length_ratio=0.3)
        self.draw()


    def start_acceleration_timer(self) -> None:
        self.Acceleration_timer = QTimer(self)
        self.Acceleration_timer.timeout.connect(self.update_acceleration_vector)
        self.Acceleration_timer.start(50)
              
        
    def update_acceleration(self,x:float,y:float,z:float) -> None:  
        self.y = round(y,1)
        self.x = round(x,1)
        self.z = round(z,1)

    def get_values(self):
        return self.target_x,self.target_y,self.target_z