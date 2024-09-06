from PySide6.QtWidgets import  QWidget
from PySide6.QtGui import QPainter, QPen, QFont, QBrush, QPolygonF, QTransform, QPixmap
from PySide6.QtCore import Qt, QPointF, QTimer, QEvent
import math
import sys


class Compass(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Digital Magnetic Compass")
        self.setMinimumSize(400, 400)
        self.current_angle = 0
        self.target_angle = 0
        self.static_pixmap = None  
        self.target_declination = 0
        self.current_declination = 0 
        self.elevation = 0 
        self.rotation = 0 
        self.start_animation_timer() 

    def resizeEvent(self, event:QEvent) -> None:

        self.create_static_pixmap()
        super().resizeEvent(event)

    def create_static_pixmap(self) -> None:
        
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

    def paintEvent(self, event: QEvent) -> None:
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

    def draw_cardinal_points(self, painter: QPainter, center: QPointF, radius:int) -> None:
        painter.setPen(QPen(Qt.black, 2))
        font = QFont("Arial", 14, QFont.Bold)
        painter.setFont(font)

        direction = {'N': 0, 'E': 90, 'S': 180, 'W': 270}
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

    def draw_lines(self, painter: QPainter, center: QPointF, radius:int) -> None:
        
        painter.setPen(QPen(Qt.black, 2))
        
        painter.drawLine(QPointF(center.x() - radius , center.y()), QPointF(center.x() + radius, center.y()))


        painter.drawLine(QPointF(center.x(), center.y() - radius ), QPointF(center.x(), center.y() + radius))

        
        split_length = 5  
        num_splits = 12 

        for i in range(num_splits):
            
            split_y = center.y() - (radius - 5) + i * (2 * (radius - 5) / (num_splits - 1)) 
            painter.drawLine(QPointF(center.x() - split_length, split_y), QPointF(center.x() + split_length, split_y))

    def draw_arrow(self, painter: QPainter, center: QPointF, radius:int) -> None:
        
        painter.setBrush(QBrush(Qt.red))
        painter.setPen(QPen(Qt.red, 2))

        
        triangle_size = 20
        arrow_distance = radius * 0.7  
        angle_rad = math.radians(self.current_angle - 90)

        
        triangle_x = center.x() + arrow_distance * math.cos(angle_rad)
        triangle_y = center.y() + arrow_distance * math.sin(angle_rad)

        
        floating_triangle = QPolygonF([
            QPointF(-triangle_size / 2, triangle_size / 2),
            QPointF(triangle_size / 2, triangle_size / 2),
            QPointF(0, -triangle_size / 2)
        ])

        
        transform = QTransform()
        transform.translate(triangle_x, triangle_y)
        transform.rotate(self.current_angle)

        rotated_triangle = transform.map(floating_triangle)
        painter.drawPolygon(rotated_triangle)

        self.draw_rotating_magnetic_north(painter, center, radius, self.current_angle, self.current_declination)

    def draw_rotating_magnetic_north(self, painter: QPainter, center: QPointF, radius: int, compass_angle: int, declination:float) -> None:
        
        painter.setBrush(QBrush(Qt.green))
        painter.setPen(QPen(Qt.green, 2))

        final_angle = declination % 360
        rad_angle = math.radians(final_angle - 90)  # -90 to align correctly

        
        marker_x = center.x() + (radius + 25) * math.cos(rad_angle)
        marker_y = center.y() + (radius + 25) * math.sin(rad_angle)

        
        marker_size = 10
        magnetic_marker = QPolygonF([
            QPointF(marker_x - marker_size / 2, marker_y),
            QPointF(marker_x + marker_size / 2, marker_y),
            QPointF(marker_x, marker_y - marker_size)
        ])

        painter.drawPolygon(magnetic_marker)

    def start_animation_timer(self)->None:
        self.azimuth_timer = QTimer(self)
        self.azimuth_timer.timeout.connect(self.__rotate_angle)
        self.azimuth_timer.start(10)  # Adjust the speed of azimuth animation

        self.declination_timer = QTimer(self)
        self.declination_timer.timeout.connect(self.__animate_declination)
        self.declination_timer.start(30)  #  Adjust the speed of declination animation

    def __rotate_angle(self)->None:
        if self.current_angle != self.target_angle:
            diff = self.target_angle - self.current_angle
            step = 1 if diff > 0 else -1

            if abs(diff) > 180:
                step *= -1

            self.current_angle = (self.current_angle + step) % 360
            self.update()

    def update_angle(self, target_angle:int) -> None:
        self.target_angle = target_angle % 360

    def update_declination(self, target_declination:float):
        self.target_declination = target_declination % 360
    

    def __animate_declination(self) -> None:
        if self.current_declination != self.target_declination:
            diff = round (self.target_declination - self.current_declination,2) # Iso : float here stick to to decimal place as a diff result
            step = 1 if diff > 0 else -1

            if abs(diff) > 180:
                step *= -1

            self.current_declination = (self.current_declination + step) % 360
            self.update()

    def set_elevation(self, elevation:float) -> None:
        self.elevation = elevation
        self.update()

    def set_rotation(self, rotation:float) -> None:
        self.rotation = rotation
        self.update()

    def draw_red_line(self, painter: QPainter, center:QPointF, radius:int):
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