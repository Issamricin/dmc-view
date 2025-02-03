from PySide6.QtCore import QPointF, Qt, QTimer
from PySide6.QtGui import QBrush, QPainter, QPen, QPolygonF, QTransform
from PySide6.QtWidgets import QApplication, QLineEdit, QMainWindow, QVBoxLayout, QWidget


class Widget(QWidget):

    def __init__(self):
        super().__init__()
        self.setMinimumSize(400, 400)
        self.angle = 0

    def paintEvent(self, event):

        painter = QPainter(self)
        pen = QPen(Qt.PenStyle.SolidLine)
        pen.setColor("black")
        pen.setWidth(4)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)
        # painter.setPen(QPen(QColor.black,4,Qt.PenCapStyle))
        # QPen(Qt.green, 3, Qt.DashDotLine, Qt.RoundCap, Qt.RoundJoin)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        center = self.rect().center()
        radius = min(self.height(), self.width()) // 2 - 20
        painter.drawEllipse(center, radius, radius)
        pen = QPen(Qt.PenStyle.SolidLine)
        pen.setColor("red")
        pen.setWidth(4)
        pen.setCapStyle(Qt.PenCapStyle.FlatCap)
        painter.setPen(pen)
        painter.setBrush(QBrush("red"))
        arrow_length = radius * 0.9

        traingle = QPolygonF([QPointF(-20, 10), QPointF(20, 10), QPointF(0, -arrow_length)])

        transform = QTransform()

        transform.translate(center.x(), center.y())
        transform.rotate(self.angle)
        self.rotated_traingle = transform.map(traingle)
        painter.drawPolygon(self.rotated_traingle)

    def update_angle(self, angle):
        self.angle = angle % 360
        self.update()


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.line = QLineEdit()
        self.line.setPlaceholderText("Enter angle in 0-360 range")
        self.line.returnPressed.connect(self.update_angle)

        self.widget = Widget()

        layout = QVBoxLayout()
        layout.addWidget(self.line)
        layout.addWidget(self.widget)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.rotate_angle)
        self.timer.start(7)

        self.current_angle = 0
        self.target_angle = 0

    def update_angle(self):
        self.target_angle = int(self.line.text()) % 360
        self.update()

    def rotate_angle(self):
        if self.target_angle != self.current_angle:
            if self.target_angle > self.current_angle:
                step = 1
            else:
                step = -1
            self.current_angle += step
            self.widget.update_angle(self.current_angle)


app = QApplication()
window = MainWindow()
window.setGeometry(200, 200, 400, 400)
window.show()
app.exec()
