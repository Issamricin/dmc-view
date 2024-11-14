import math
import sys

from PySide6.QtCore import QPointF, Qt, QTimer
from PySide6.QtGui import QBrush, QFont, QPainter, QPen, QPolygonF, QTransform
from PySide6.QtWidgets import QApplication, QLineEdit, QMainWindow, QVBoxLayout, QWidget


class Compass(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(400, 400)
        self.angle = 0

    def paintEvent(self, event):

        painter = QPainter(self)
        pen = QPen(Qt.PenStyle.SolidLine)
        pen.setColor("black")
        pen.setWidth(4)
        painter.setPen(pen)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Offset for the circle to be to the left
        x_offset = 70
        center = QPointF(self.rect().center().x() - x_offset, self.rect().center().y())
        radius = min(self.width() - 2 * x_offset, self.height()) // 2 - 30

        painter.drawEllipse(center, radius, radius)

        self.draw_cardinal_points(painter, center, radius)

        self.draw_arrow(painter, center, radius)

        text_x = center.x() + radius + 100
        text_y = center.y() - radius
        test_pos = QPointF(text_x, text_y)

        painter.drawText(test_pos, "Information")

    def draw_cardinal_points(self, painter, center, radius):
        painter.setPen(QPen(Qt.black, 2))
        font = QFont("Arial", 14, QFont.Bold)
        painter.setFont(font)

        direction = {"N": 0, "E": 90, "S": 180, "W": 270}
        for lable, angle in direction.items():
            rad_angle = math.radians(angle - 90)
            x = center.x() + (radius + 15) * math.cos(rad_angle)
            y = center.y() + (radius + 15) * math.sin(rad_angle)

            text_rect = painter.fontMetrics().boundingRect(lable)
            text_x = x - text_rect.width() / 2
            text_y = y + text_rect.height() / 2

            painter.drawText(QPointF(text_x, text_y), lable)

        for angle in range(0, 360, 30):
            rad_angle = math.radians(angle)
            outer_x = center.x() + radius * math.cos(rad_angle)
            outer_y = center.y() + radius * math.sin(rad_angle)
            inner_x = center.x() + (radius - 10) * math.cos(rad_angle)
            inner_y = center.y() + (radius - 10) * math.sin(rad_angle)

            painter.drawLine(QPointF(outer_x, outer_y), QPointF(inner_x, inner_y))

    def draw_arrow(self, painter, center, radius):
        painter.setBrush(QBrush(Qt.red))

        arrow_length = radius * 0.9

        red_triangle = QPolygonF(
            [QPointF(-20, 10), QPointF(20, 10), QPointF(0, -arrow_length)]
        )
        white_triangle = QPolygonF(
            [QPointF(-20, 10), QPointF(20, 10), QPointF(0, arrow_length)]
        )

        transform = QTransform()
        transform.translate(center.x(), center.y())
        transform.rotate(self.angle)
        red_rotated_triangle = transform.map(red_triangle)
        white_rotated_triangle = transform.map(white_triangle)
        painter.drawPolygon(red_rotated_triangle)
        painter.setBrush(QBrush(Qt.white))
        painter.drawPolygon(white_rotated_triangle)

    def update_angle(self, angle):
        self.angle = angle % 360
        self.update()


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.compass = Compass()

        self.line = QLineEdit()
        self.line.setPlaceholderText("Enter angle between 0-360 %")
        self.line.returnPressed.connect(self.update_angle)

        layout = QVBoxLayout()
        layout.addWidget(self.compass)
        layout.addWidget(self.line)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.current_angle = 0
        self.target_angle = 0

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.rotate_angle)
        self.timer.start(10)

    def update_angle(self):

        self.target_angle = int(self.line.text()) % 360

    def rotate_angle(self):

        if self.current_angle != self.target_angle:
            diff = self.target_angle - self.current_angle
            step = 1 if diff > 0 else -1

            if abs(diff) > 180:
                step *= -1

            self.current_angle = (self.current_angle + step) % 360

            self.compass.update_angle(self.current_angle)


app = QApplication(sys.argv)
window = Window()
window.show()
app.exec()
