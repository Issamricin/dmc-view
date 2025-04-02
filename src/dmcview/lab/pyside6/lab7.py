from PySide6.QtCore import QPointF, QRectF, Qt
from PySide6.QtGui import QPainter, QPen
from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget


class CompassWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.bank_angle = 90  # Bank angle in degrees

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Draw the lines and arc
        self.draw_lines_and_arc(painter)
        
    def draw_lines_and_arc(self, painter):

        pen = QPen(Qt.black, 2)
        painter.setPen(pen)


        center = QPointF(self.width() / 2, self.height() / 2)
        radius = min(self.width(), self.height()) / 2 - 10
        

        start_x = center.x() - radius
        end_x = center.x() + radius
        painter.drawLine(QPointF(start_x, center.y()), QPointF(end_x, center.y()))
        

        painter.drawLine(QPointF(center.x(), center.y() - radius), QPointF(center.x(), center.y() + radius))
        

        start_angle = 0 # Starting angle (in degrees) for the horizontal line
        span_angle = self.bank_angle  # Bank angle (in degrees)
        
        rect = QRectF(center.x() - radius, center.y() - radius, 2 * radius, 2 * radius)
        
        # Qt need angel in 1/16th degree
        start_angle *= 16
        span_angle *= 16
        
        pen.setColor(Qt.red)
        painter.setPen(pen)
        painter.drawArc(rect, int(start_angle), int(span_angle))

class CompassApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Arc Between Lines Demo")
        self.setGeometry(100, 100, 400, 400)
        
        layout = QVBoxLayout()
        self.compass_widget = CompassWidget()
        layout.addWidget(self.compass_widget)
        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication([])
    window = CompassApp()
    window.show()
    app.exec()
