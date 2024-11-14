# Drawing a circle that remains at the center of the widget/screen
from PySide6.QtGui import QPainter, QPen, Qt
from PySide6.QtWidgets import QApplication, QWidget


class Circle(QWidget):
    def __init__(self):
        super().__init__()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(QPen(Qt.black, 4, Qt.SolidLine))

        # Draw the circle
        center = self.rect().center()
        radius = min(self.width(), self.height()) // 2 - 20
        painter.drawEllipse(center, radius, radius)


app = QApplication()
window = Circle()
window.show()
app.exec()
