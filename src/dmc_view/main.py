from compass import Compass
from PySide6.QtWidgets import QApplication


def main():
    app = QApplication()
    compass = Compass()
    compass.show()
    compass.update_declination(10)  #
    compass.update_angle(
        35
    )  # This is Azimuth and can be float to two decimal places for example 35.55
    app.exec()


main()
