# A label that follows a line at any angle
import sys
from math import cos, radians, sin

from PySide6.QtCore import QRectF, Qt
from PySide6.QtGui import QFont, QPainter, QPen
from PySide6.QtWidgets import QApplication, QLineEdit, QPushButton, QVBoxLayout, QWidget


class RotatingLineWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.angle = 0  
        self.setMinimumSize(400, 400)

        self.input = QLineEdit(self)
        self.input.setPlaceholderText("Enter angle in degrees")

        # Button to update angle
        self.button = QPushButton("Rotate Line", self)
        self.button.clicked.connect(self.update_angle)

        # Layout for buttons at the bottom
        layout = QVBoxLayout()
        layout.addStretch()
        layout.addWidget(self.input)
        layout.addWidget(self.button)

        self.setLayout(layout)

    def update_angle(self):
            # Update the angle from the user input
            self.angle = float(self.input.text())
            self.update()  # Trigger a repaint of the widget

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        center_x = self.width() // 2
        center_y = self.height() // 2 - 50

        line_length = 100
        line_start = (center_x, center_y)


        angle_radians = radians(self.angle)
        line_end_x = center_x + line_length * sin(angle_radians)
        line_end_y = center_y - line_length * cos(angle_radians)

        pen = QPen(Qt.black, 4)
        painter.setPen(pen)
        painter.setFont(QFont("Arial", 12))


        painter.drawLine(line_start[0], line_start[1], line_end_x, line_end_y)


        painter.resetTransform()

        label_x = line_end_x - 30 
        label_y = line_end_y - 20  
        painter.drawText(QRectF(label_x, label_y, 50, 20), Qt.AlignCenter, "Label")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RotatingLineWidget()
    window.show()
    sys.exit(app.exec())
