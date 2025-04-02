import math

from PySide6.QtCore import QPointF, Qt, QTimer
from PySide6.QtGui import QBrush, QFont, QPainter, QPen, QPixmap, QPolygonF, QTransform
from PySide6.QtWidgets import QApplication, QLineEdit, QMainWindow, QVBoxLayout, QWidget


class Compass(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(400, 400)
        self.angle = 0
        self.static_pixmap = None
        self.declination = 0
        self.current_declination = 0
        self.elevation = 0
        self.rotation = 0

    def resizeEvent(self, event):

        self.create_static_pixmap()
        super().resizeEvent(event)

    def create_static_pixmap(self):

        self.static_pixmap = QPixmap(self.size())
        self.static_pixmap.fill(Qt.transparent)

        painter = QPainter(self.static_pixmap)
        pen = QPen(Qt.PenStyle.SolidLine)
        pen.setColor("black")
        pen.setWidth(4)
        painter.setPen(pen)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Offset for the circle to be to the left
        x_offset = 70
        center = QPointF(self.rect().center().x() - x_offset, self.rect().center().y())
        radius = min(self.width() - 2 * x_offset, self.height()) // 2 - 30

        # Drawing on the pixmap
        painter.drawEllipse(center, radius, radius)
        self.draw_cardinal_points(painter, center, radius)
        self.draw_lines(painter, center, radius)

        painter.end()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        if self.static_pixmap:
            painter.drawPixmap(0, 0, self.static_pixmap)

        x_offset = 70
        center = QPointF(self.rect().center().x() - x_offset, self.rect().center().y())
        radius = min(self.width() - 2 * x_offset, self.height()) // 2 - 30
        self.draw_arrow(painter, center, radius)

        self.draw_red_line(painter, center, radius)

        painter.setPen(QPen(Qt.black))
        text_x = center.x() + radius + 100
        text_y = center.y() - radius
        test_pos = QPointF(text_x, text_y)
        painter.drawText(test_pos, "Information")

    def draw_cardinal_points(self, painter, center, radius):
        painter.setPen(QPen(Qt.black, 2))
        font = QFont("Arial", 14, QFont.Bold)
        painter.setFont(font)

        direction = {"N": 0, "E": 90, "S": 180, "W": 270}
        for label, angle in direction.items():
            rad_angle = math.radians(angle - 90)
            x = center.x() + (radius + 15) * math.cos(rad_angle)
            y = center.y() + (radius + 15) * math.sin(rad_angle)

            text_rect = painter.fontMetrics().boundingRect(label)
            text_x = x - text_rect.width() / 2
            text_y = y + text_rect.height() / 2

            painter.drawText(QPointF(text_x, text_y), label)

        for angle in range(0, 360, 30):
            rad_angle = math.radians(angle)
            outer_x = center.x() + radius * math.cos(rad_angle)
            outer_y = center.y() + radius * math.sin(rad_angle)
            inner_x = center.x() + (radius - 10) * math.cos(rad_angle)
            inner_y = center.y() + (radius - 10) * math.sin(rad_angle)

            painter.drawLine(QPointF(outer_x, outer_y), QPointF(inner_x, inner_y))

    def draw_lines(self, painter, center, radius):

        painter.setPen(QPen(Qt.black, 2))

        painter.drawLine(
            QPointF(center.x() - radius, center.y()), QPointF(center.x() + radius, center.y())
        )

        painter.drawLine(
            QPointF(center.x(), center.y() - radius), QPointF(center.x(), center.y() + radius)
        )

        split_length = 5
        num_splits = 12

        for i in range(num_splits):

            split_y = center.y() - (radius - 5) + i * (2 * (radius - 5) / (num_splits - 1))
            painter.drawLine(
                QPointF(center.x() - split_length, split_y),
                QPointF(center.x() + split_length, split_y),
            )

    def draw_arrow(self, painter, center, radius):

        painter.setBrush(QBrush(Qt.red))
        painter.setPen(QPen(Qt.red, 2))

        triangle_size = 20
        arrow_distance = radius * 0.7
        angle_rad = math.radians(self.angle - 90)

        triangle_x = center.x() + arrow_distance * math.cos(angle_rad)
        triangle_y = center.y() + arrow_distance * math.sin(angle_rad)

        floating_triangle = QPolygonF(
            [
                QPointF(-triangle_size / 2, triangle_size / 2),
                QPointF(triangle_size / 2, triangle_size / 2),
                QPointF(0, -triangle_size / 2),
            ]
        )

        transform = QTransform()
        transform.translate(triangle_x, triangle_y)
        transform.rotate(self.angle)

        rotated_triangle = transform.map(floating_triangle)
        painter.drawPolygon(rotated_triangle)

        self.draw_rotating_magnetic_north(
            painter, center, radius, self.angle, self.current_declination
        )

    def draw_rotating_magnetic_north(
        self, painter, center, radius, compass_angle, declination
    ):

        painter.setBrush(QBrush(Qt.green))
        painter.setPen(QPen(Qt.green, 2))

        final_angle = declination % 360
        rad_angle = math.radians(final_angle - 90)  # -90 to align correctly

        marker_x = center.x() + (radius + 25) * math.cos(rad_angle)
        marker_y = center.y() + (radius + 25) * math.sin(rad_angle)

        marker_size = 10
        magnetic_marker = QPolygonF(
            [
                QPointF(marker_x - marker_size / 2, marker_y),
                QPointF(marker_x + marker_size / 2, marker_y),
                QPointF(marker_x, marker_y - marker_size),
            ]
        )

        painter.drawPolygon(magnetic_marker)

    def update_angle(self, angle):
        self.angle = angle % 360
        self.update()

    def update_declination(self, declination):
        self.declination = declination % 360
        self.animate_declination()

    def animate_declination(self):
        if self.current_declination != self.declination:
            diff = self.declination - self.current_declination
            step = 1 if diff > 0 else -1

            if abs(diff) > 180:
                step *= -1

            self.current_declination = (self.current_declination + step) % 360
            self.update()

    def set_elevation(self, elevation):
        self.elevation = elevation
        self.update()

    def set_rotation(self, rotation):
        self.rotation = rotation
        self.update()

    def draw_red_line(self, painter, center, radius):
        painter.setPen(QPen(Qt.red, 2))

        line_length = radius * 2
        transform = QTransform()
        transform.translate(center.x(), center.y())
        transform.rotate(-self.rotation)
        transform.translate(0, -self.elevation)

        line_start = QPointF(-line_length / 2, 0)
        line_end = QPointF(line_length / 2, 0)
        transformed_line = transform.map(QPolygonF([line_start, line_end]))

        painter.drawLine(transformed_line[0], transformed_line[1])


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.compass = Compass()

        self.angle_input = QLineEdit()
        self.angle_input.setPlaceholderText("Enter angle between 0-360°")
        self.angle_input.returnPressed.connect(self.update_angle)

        self.declination_input = QLineEdit()
        self.declination_input.setPlaceholderText("Enter magnetic declination")
        self.declination_input.returnPressed.connect(self.update_declination)

        self.elevation_input = QLineEdit()
        self.elevation_input.setPlaceholderText("Enter elevation angle")
        self.elevation_input.returnPressed.connect(self.update_elevation)

        self.rotation_input = QLineEdit()
        self.rotation_input.setPlaceholderText("Enter rotation angle")
        self.rotation_input.returnPressed.connect(self.update_rotation)

        layout = QVBoxLayout()
        layout.addWidget(self.compass)
        layout.addWidget(self.angle_input)
        layout.addWidget(self.declination_input)
        layout.addWidget(self.elevation_input)
        layout.addWidget(self.rotation_input)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.current_angle = 0
        self.target_angle = 0

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.rotate_angle)
        self.timer.start(10)

        self.declination_timer = QTimer(self)
        self.declination_timer.timeout.connect(self.compass.animate_declination)
        self.declination_timer.start(20)  # Adjust the speed of declination animation

    def update_angle(self):
        self.target_angle = int(self.angle_input.text()) % 360

    def update_declination(self):
        try:
            declination = float(self.declination_input.text())
            self.compass.update_declination(declination)
        except ValueError:
            print("Invalid declination value. Please enter a number.")

    def update_elevation(self):
        try:
            elevation = float(self.elevation_input.text())
            self.compass.set_elevation(elevation)
        except ValueError:
            print("Invalid elevation value. Please enter a number.")

    def update_rotation(self):
        try:
            rotation = float(self.rotation_input.text())
            self.compass.set_rotation(rotation)
        except ValueError:
            print("Invalid rotation value. Please enter a number.")

    def rotate_angle(self):
        if self.current_angle != self.target_angle:
            diff = self.target_angle - self.current_angle
            step = 1 if diff > 0 else -1

            if abs(diff) > 180:
                step *= -1

            self.current_angle = (self.current_angle + step) % 360
            self.compass.update_angle(self.current_angle)


app = QApplication()
window = Window()
window.show()
app.exec()
