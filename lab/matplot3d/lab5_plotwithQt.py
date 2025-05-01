from PySide6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

class Matplotlib3DWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Create a Matplotlib figure and canvas
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        # Create a layout and add the canvas
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        # Plot 3D example
        self.plot_3d_example()

    def plot_3d_example(self):
        """Plots a 3D surface example."""
        ax = self.figure.add_subplot(111, projection="3d")  # 3D Axes

        # Generate data
        X = np.linspace(-5, 5, 50)
        Y = np.linspace(-5, 5, 50)
        X, Y = np.meshgrid(X, Y)
        Z = np.sin(np.sqrt(X**2 + Y**2))  # Example surface function

        # Create 3D surface plot
        ax.plot_surface(X, Y, Z, cmap="viridis")

        # Update the canvas
        self.canvas.draw()



from PySide6.QtWidgets import QMainWindow, QApplication
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create and set the Matplotlib3DWidget as the central widget
        self.matplotlib_widget = Matplotlib3DWidget(self)
        self.setCentralWidget(self.matplotlib_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
