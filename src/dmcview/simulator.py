from random import uniform

from PySide6.QtCore import (
    QEvent,
    QObject,
    QRunnable,
    QThread,
    QThreadPool,
    Signal,
    Slot,
)
from PySide6.QtWidgets import QApplication, QHBoxLayout, QWidget

from dmcview.acceleration import Accelaration3D
from dmcview.compass import Compass


class SimulatorSignal(QObject):
    """Define the signals available from a running worker thread"""

    result = Signal(
        str, str, str, str, str, str
    )  # azimuth, elevation, bank and acceleration (x,y,z)


class SimulatorRunner(QRunnable):
    """class extends QRunnable to run in a separate thread.

       It generates random values for azimuth, elevation (inclination), bank, and acceleration.

       """
    def __init__(self) -> None:
        super().__init__()
        self.signal = SimulatorSignal()
        self.running = True

    @Slot()
    def run(self) -> None:
        while self.running:
            azimuth = round(uniform(20.0, 40.0), 2)
            inclination = round(uniform(20.0, 35.0), 2)
            bank = round(uniform(30.0, 45.0), 2)
            x = round(uniform(5.0, 15.0), 1)
            y = x
            z = 0.0

            print(
                f"Azimuth:{azimuth}; Inclination(Elevation):{inclination}; Bank(Rotation):{bank}; acceleration:{ [x, y, z]}"
            )
            self.signal.result.emit(
                str(azimuth), str(inclination), str(bank), str(x), str(y), str(z)
            )
            QThread.sleep(2)  # two seconds

    def stop(self) -> None:
        self.running = False


class Simulator(QWidget):
    """
    This class represents the main GUI.

    The simulator class Load, initiate and keep track of all models being simulated,Keep track of time,
    Initialize the plots.
    """
    def __init__(self) -> None:
        super().__init__()
        self.threadPool = QThreadPool()
        self.runner = SimulatorRunner()

        layout = QHBoxLayout(self)
        self.compass = Compass()
        layout.addWidget(self.compass)

        self.canvas = Accelaration3D()
        self.canvas.setFixedSize(350, 350)
        layout.addWidget(self.canvas)

        self.runner.signal.result.connect(self.__update)
        self.threadPool.start(self.runner)

        self.compass.update_declination(10.5)
        self.setWindowTitle("Simulator")

    def __update(
        self, azimuth: str, elevation: str, bank: str, x: str, y: str, z: str
    ) -> None:
        """
        This method update the compass new values from SimulatorRunner class .
        """
        self.compass.update_angle(float(azimuth))
        self.compass.set_elevation(float(elevation))
        self.compass.set_rotation(float(bank))
        self.canvas.update_acceleration(
            round(float(x), 1), round(float(y), 1), round(float(z), 1)
        )

    def closeEvent(self, event: QEvent) -> None:
        # Stop any running threads/timers/simulations here
        print("Shutting down simulator ...")
        self.runner.stop()
        event.accept()


def start_simulator() -> None:
    app = QApplication()
    sim = Simulator()
    sim.show()
    app.exec()


if __name__ == "__main__":  # this is import so that it does not run from pytest
    start_simulator()
