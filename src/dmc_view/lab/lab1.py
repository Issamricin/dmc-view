import os
import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import (
    QImage,
    QKeySequence,
    QMouseEvent,
    QPainter,
    QPaintEvent,
    QShortcut,
)
from PySide6.QtWidgets import QApplication, QGridLayout, QMainWindow, QWidget


class Canvas(QWidget):

    def __init__(self, photo, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.image = QImage(photo)
        self.setFixedSize(self.image.width(), self.image.height())
        self.pressed = self.moving = False
        self.revisions = []

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.pressed = True
            self.center = event.position()
            self.update()

    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() & Qt.MouseButton.LeftButton:
            self.moving = True
            r = (event.pos().x() - self.center.x()) ** 2 + (
                event.pos().y() - self.center.y()
            ) ** 2
            self.radius = r**0.5
            self.update()

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.revisions.append(self.image.copy())
            qp = QPainter(self.image)
            self.draw_circle(qp) if self.moving else self.draw_point(qp)
            self.pressed = self.moving = False
            self.update()

    def paintEvent(self, event: QPaintEvent):
        qp = QPainter(self)
        qp.drawImage(event.rect(), self.image, event.rect())
        if self.moving:
            self.draw_circle(qp)
        elif self.pressed:
            self.draw_point(qp)

    def draw_point(self, qp: QPainter):
        qp.setPen(Qt.PenStyle.DashLine)
        qp.drawPoint(self.center)

    def draw_circle(self, qp: QPainter):
        qp.setRenderHint(QPainter.RenderHint.Antialiasing)
        qp.setPen(Qt.PenStyle.DashLine)
        qp.drawEllipse(self.center, self.radius, self.radius)

    def undo(self):
        if self.revisions:
            self.image = self.revisions.pop()
            self.update()

    def reset(self):
        if self.revisions:
            self.image = self.revisions[0]
            self.revisions.clear()
            self.update()


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        w = QWidget()
        # You see how to refer to an image since the runtime goes to the workspace directory which
        # static based on user workspace location(absolute path)
        base = os.path.dirname(__file__)
        image_location = os.path.join(base, "images")
        # print(image_location) I do this as a debug statement sometime it helps
        self.setCentralWidget(w)
        canvas = Canvas(image_location + "/lab1.png")
        grid = QGridLayout(w)
        grid.addWidget(canvas)
        QShortcut(QKeySequence("Ctrl+Z"), self, canvas.undo)
        QShortcut(QKeySequence("Ctrl+R"), self, canvas.reset)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = MainWindow()
    gui.show()
    sys.exit(app.exec())
