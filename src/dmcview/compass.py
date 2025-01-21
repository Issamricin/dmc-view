import math

from PySide6.QtCore import QEvent, QPointF, QRectF, Qt, QTimer
from PySide6.QtGui import (
    QBrush,
    QColor,
    QFont,
    QPainter,
    QPen,
    QPixmap,
    QPolygonF,
    QResizeEvent,
    QTransform,
)
from PySide6.QtWidgets import QWidget


class Compass(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Digital Magnetic Compass")
        self.setMinimumSize(600, 420)
        self.current_angle = 0.0
        self.target_angle = 0.0
        self.target_declination = 0.0
        self.current_declination = 0.0
        self.elevation = 0.0
        self.rotation = 0.0
        self.start_animation_timer()

    def resizeEvent(self, event: QResizeEvent) -> None:
        """
        triggers when screen resize happens
        
        Args:
            event (QResizeEvent) : The QT size event
        
        """ 

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
        radius = min(self.width() - 2 * x_offset, self.height()) // 2 - 37

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
        radius = min(self.width() - 2 * x_offset, self.height()) // 2 - 37
        self.draw_arrow(painter, center, radius)

        self.draw_red_line(painter, center, radius)

        font_size = max(12,self.width()//80)
        line_spacing = font_size

        painter.setPen(QPen(Qt.black))
        painter.setFont(QFont("Arial",font_size))
        text_x = center.x() + radius + 60 # reduce the number to prevent capped text
        text_y = center.y() - radius

        test_pos = QPointF(text_x, text_y)
        azimuth_pos = QPointF(text_x,text_y + 4 * line_spacing)
        declination_pos = QPointF(text_x,text_y + 8 * line_spacing)
        rotation_pos = QPointF(text_x,text_y + 12 * line_spacing)
        inclination_pos = QPointF(text_x,text_y + 16 * line_spacing)

        painter.drawText(test_pos, "Information: ")
        painter.drawText(azimuth_pos,f"Azimuth: {round(self.current_angle,2)} °")
        painter.drawText(declination_pos,f"Declination: {round(self.current_declination,2)} °")
        painter.drawText(rotation_pos,f"Bank: {round(self.rotation,2)} °")
        painter.drawText(inclination_pos,f"Elevation: {round(self.elevation,2)} °")

    def draw_cardinal_points(self, painter: QPainter, center: QPointF, radius: int) -> None:
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

    def draw_lines(self, painter: QPainter, center: QPointF, radius: int) -> None:

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

    def draw_arrow(self, painter: QPainter, center: QPointF, radius: int) -> None:

        painter.setBrush(QBrush(Qt.red))
        painter.setPen(QPen(Qt.red, 2))

        triangle_size = 20
        arrow_distance = radius * 0.8
        angle_rad = -math.radians(self.elevation)

        triangle_x = center.x() + arrow_distance * math.cos(angle_rad)
        triangle_y = center.y() + arrow_distance * math.sin(angle_rad)

        pen = QPen(Qt.red,1,Qt.SolidLine) 
        pen2 = QPen(QColor("DarkBlue"),1,Qt.DashLine)

        painter.setPen(pen)

        painter.drawLine(center.x(),center.y(),triangle_x,triangle_y)

        floating_triangle = QPolygonF(
            [
                QPointF(-triangle_size / 2, triangle_size / 2),
                QPointF(triangle_size / 2, triangle_size / 2),
                QPointF(0, -triangle_size / 2),
            ]
        )

        transform = QTransform()
        transform.translate(triangle_x, triangle_y)
        transform.rotate(90-self.elevation)

        rotated_triangle = transform.map(floating_triangle)
        painter.drawPolygon(rotated_triangle)


        pen = QPen(Qt.black,1,Qt.DashLine) 
        painter.setPen(pen)

        arc2_radius = radius - 120
        rect2 = QRectF(center.x() - arc2_radius,center.y() - arc2_radius, 2 * arc2_radius, 2 * arc2_radius)
        startAngleIncli = 0 *16 # Inclination

        if (self.elevation>270): # it is maxed at 90 but 
            spanAngleIncli = 90 * 16.00 # make it float
        elif (self.elevation>90):
            spanAngleIncli = 0.00 # make it float
        else:
            spanAngleIncli = ( self.elevation) * 16 # float datatype (implicit)
  
        painter.resetTransform()

        midPointAngelIncli = startAngleIncli + spanAngleIncli / 2 # Inclination
        mid_angel_rad_incli = math.radians(midPointAngelIncli / 16)

        midpoint_incli_x = center.x() + arc2_radius * math.cos(mid_angel_rad_incli) # Inclination
        midpoint_incli_y = center.y() - arc2_radius * math.sin(mid_angel_rad_incli)

        label2 = "Elevation"

        painter.setPen(pen2)
        painter.drawArc(rect2, int(startAngleIncli), int(spanAngleIncli))
        painter.drawText(QPointF(midpoint_incli_x + 11,midpoint_incli_y - 10), label2) # Inclination

        self.draw_rotating_magnetic_north(
            painter, center, radius, self.current_angle, self.current_declination
        )

        self.draw_azimuth(
            painter, center, radius, self.current_angle
        )

    def draw_rotating_magnetic_north(
        self,
        painter: QPainter,
        center: QPointF,
        radius: int,
        compass_angle: float,
        declination: float,
    ) -> None:
        
        dark_red = QColor(124,10,2)

        painter.setBrush(dark_red)
        painter.setPen(QPen(dark_red, 2))

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

        painter.resetTransform()

        
        pen = QPen(dark_red,1,Qt.DashLine) 
        painter.setPen(pen)

        arc_radius = radius + 25

        rect = QRectF(center.x() - arc_radius,center.y() - arc_radius, 2 * arc_radius, 2 * arc_radius)

        startAngle = 90 * 16 

        if(self.current_declination>180):
            spanAngle = (360 - self.current_declination)  * 16 
        else: 
            spanAngle = -self.current_declination * 16 # angle in 1/16th degree expected by Qt

    
        painter.drawArc(rect, int(startAngle), int(spanAngle))


        midPointAngel = startAngle + spanAngle / 2
        AngelRad = math.radians(midPointAngel/16)

        midPoint_x = center.x() + arc_radius * math.cos(AngelRad)
        midPoint_y = center.y() - arc_radius * math.sin(AngelRad)

        label = "Declination"

        if self.current_declination < 180: # each side has different alignment 
            painter.drawText(QPointF(midPoint_x + 50,midPoint_y + 1 ),label) # +7 so it is not touching with the arc
        else:
            painter.drawText(QPointF(midPoint_x - 100,midPoint_y ),label) # -90 so it is not touching the circle

    def draw_azimuth(
        self,
        painter: QPainter,
        center: QPointF,
        radius: int,
        compass_angle: float,
    ) -> None:
        
        dark_green = QColor(87,108,67)

        painter.setBrush(dark_green)
        painter.setPen(QPen(dark_green, 2))

        final_angle = compass_angle % 360
        rad_angle = math.radians(final_angle - 90)  # -90 to align correctly

        marker_x = center.x() + (radius -20) * math.cos(rad_angle)
        marker_y = center.y() + (radius -20) * math.sin(rad_angle)

        marker_size = 10
        magnetic_marker = QPolygonF(
            [
                QPointF(marker_x - marker_size / 2, marker_y),
                QPointF(marker_x + marker_size / 2, marker_y),
                QPointF(marker_x, marker_y - marker_size),
            ]
        )

        painter.drawPolygon(magnetic_marker)

        painter.resetTransform()

        
        pen = QPen(dark_green,1,Qt.DashLine) 
        painter.setPen(pen)

        arc_radius = radius - 20

        rect = QRectF(center.x() - arc_radius,center.y() - arc_radius, 2 * arc_radius, 2 * arc_radius)

        startAngle = 90 * 16 

        if(self.current_angle>180):
            spanAngle = (360 - self.current_angle)  * 16 
        else: 
            spanAngle = -self.current_angle * 16 # angle in 1/16th degree expected by Qt

    
        painter.drawArc(rect, int(startAngle), int(spanAngle))


        midPointAngel = startAngle + spanAngle / 2
        AngelRad = math.radians(midPointAngel/16)

        midPoint_x = center.x() + arc_radius * math.cos(AngelRad)
        midPoint_y = center.y() - arc_radius * math.sin(AngelRad)

        label = "Azimuth"

        if self.current_angle == 0: # each side has different alignment 
            painter.drawText(QPointF(midPoint_x+12,midPoint_y+22),label)
        elif self.current_angle < 180: # each side has different alignment 
            painter.drawText(QPointF(midPoint_x-25,midPoint_y+25),label) 
        else:
            painter.drawText(QPointF(midPoint_x-10,midPoint_y+25),label)


    def start_animation_timer(self) -> None:
        self.azimuth_timer = QTimer(self)
        self.azimuth_timer.timeout.connect(self.__rotate_angle)
        self.azimuth_timer.start(1)  # Adjust the speed of azimuth animation

        self.declination_timer = QTimer(self)
        self.declination_timer.timeout.connect(self.__animate_declination)
        self.declination_timer.start(2)  #  Adjust the speed of declination animation

    def __rotate_angle(self) -> None:
        if self.current_angle != self.target_angle:
            diff = round(self.target_angle - self.current_angle, 2)  # Here is for the azimuth
            step = 0.1 if diff > 0 else -0.1

            if abs(diff) > 180:
                step *= -1

            if abs(diff) < 0.2:
                self.current_angle = self.target_angle
            else:
                self.current_angle = (self.current_angle + step) % 360
            self.update()

    def update_angle(self, target_angle: float) -> None:
        self.target_angle = target_angle % 360

    def update_declination(self, target_declination: float):
        self.target_declination = target_declination % 360

    def __animate_declination(self) -> None:
        if self.current_declination != self.target_declination:
            diff = round(
                self.target_declination - self.current_declination, 2
            )  # Iso : float here stick to to decimal place as a diff result
            step = 0.1 if diff > 0 else -0.1

            if abs(diff) > 180:
                step *= -1

            if abs(diff) < 0.2:
                self.current_declination = self.target_declination
            else:
                self.current_declination = (self.current_declination + step) % 360
            self.update()

    def set_elevation(self, elevation: float) -> None:
        self.elevation = elevation
        self.update()

    def set_rotation(self, rotation: float) -> None:
        self.rotation = rotation
        self.update()

    def draw_red_line(self, painter: QPainter, center: QPointF, radius: int) -> None:
        painter.setPen(QPen(Qt.red, 2))

        line_length = radius * 2
        transform = QTransform()
        transform.translate(center.x(), center.y())
        transform.rotate(-self.rotation)

        line_start = QPointF(-line_length / 2, 0)
        line_end = QPointF(line_length / 2, 0)
        transformed_line = transform.map(QPolygonF([line_start, line_end]))

        painter.drawLine(transformed_line[0], transformed_line[1])

        
        pen = QPen(Qt.black,1,Qt.DashLine) 
        painter.setPen(pen)

        arc_radius = radius - 40 # -40 so it is not touching the circle

        rect = QRectF(center.x() - arc_radius,center.y() - arc_radius, 2 * arc_radius, 2 * arc_radius)

        startAngle = 16 * 180 # *180 so it is draw to the left of the circle
        spanAngle = self.rotation * 16 # angle in 1/16th degree expected by Qt

    
        painter.drawArc(rect, int(startAngle), int(spanAngle))

        midPointAngel = startAngle + spanAngle / 2
        mid_angel_rad = math.radians(midPointAngel / 16) # angle in 1/16th degree expected by Qt


        midpoint_x = center.x() + arc_radius * math.cos(mid_angel_rad) + 10 #offset to the right 10 so it is not touching the arc
        midpoint_y = center.y() - arc_radius * math.sin(mid_angel_rad)

        label = "Bank"
        painter.drawText(QPointF(midpoint_x,midpoint_y - 2), label) # -2 so it is not touching line at 0 angle
