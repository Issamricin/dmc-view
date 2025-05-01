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

        self.counter = 0.0
        self.value = 0.2 #0.1 step is very slow
        self.accela = round(float(input("Enter your accelaration value: ")),1)

        last_digit = self.accela*10
        last_digit = last_digit %10
        if last_digit % 2 != 0:
            self.accela += 0.1  #since the step is 0.2 we will make odd inputs into even.

        self.ax.set_xlim([-15, 15])
        self.ax.set_ylim([-15, 15])
        self.ax.set_zlim([-15, 15])
        self.ax.set_xlabel("X Axis")
        self.ax.set_ylabel("Y Axis")
        self.ax.set_zlabel("Z Axis")
        self.ax.set_title("Acceleration 3D")

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateAcceleration)
        self.timer.start(100)

    def updateAcceleration(self):
        self.ax.clear()

        self.ax.set_xlim([-15, 15])
        self.ax.set_ylim([-15, 15])
        self.ax.set_zlim([-15, 15])
        self.ax.set_xlabel("X Axis")
        self.ax.set_ylabel("Y Axis")
        self.ax.set_zlabel("Z Axis")
        self.ax.set_title("Dynamic 3D Acceleration")

        accel = np.array([self.counter,self.counter,0])
        origin= np.array([0,0,0])

        self.ax.quiver(*origin, *accel, color="Red", linewidth=2, arrow_length_ratio=0.3)

        self.canvas.draw()

        self.counter = round(self.counter,1)
        print(self.counter)

        if self.counter < self.accela:
            self.counter += self.value
        elif self.counter > self.accela:
            self.counter -= self.value

    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DynamicAccelaration3D()
    window.show()
    sys.exit(app.exec_())