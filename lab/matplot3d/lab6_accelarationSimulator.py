import numpy as np
import sys
from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget
from PySide6.QtCore import QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class DynamicAccelaration3D(QWidget):
    def __init__(self, parent =None):
        super().__init__(parent)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        self.ax = self.figure.add_subplot(projection='3d')

        self.counter = 0
        self.value = 0.2
        self.max_acceleration = 6
        self.min_acceleration = 0

        self.ax.set_xlim([-6,6])
        self.ax.set_ylim([-6,6])
        self.ax.set_zlim([-6,6])
        self.ax.set_xlabel("X Axis")
        self.ax.set_ylabel("Y Axis")
        self.ax.set_zlabel("Z Axis")
        self.ax.set_title("Acceleration 3D")

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateAcceleration)
        self.timer.start(100)

    def updateAcceleration(self):
        self.ax.clear()

        self.ax.set_xlim([-6, 6])
        self.ax.set_ylim([-6, 6])
        self.ax.set_zlim([-6, 6])
        self.ax.set_xlabel("X Axis")
        self.ax.set_ylabel("Y Axis")
        self.ax.set_zlabel("Z Axis")
        self.ax.set_title("Dynamic 3D Acceleration")

        accel = np.array([self.counter,self.counter,0])
        origin= np.array([0,0,0])

        self.ax.quiver(*origin, *accel, color="Red", linewidth=2, arrow_length_ratio=0.3)

        self.canvas.draw()

        if self.counter > self.max_acceleration:
            self.value *= -1

        if self.counter < self.min_acceleration:
            self.value *= -1
        
        self.counter += self.value

    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DynamicAccelaration3D()
    window.show()
    sys.exit(app.exec_())