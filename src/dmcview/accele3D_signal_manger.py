#signal that sends acceleration data from acceleration to compass class
from PySide6.QtCore import QObject, Signal

class AccelerationSignalManager(QObject):
    data_signal = Signal(float, float, float)  # Signal that sends three float values (x, y, z)

    def __init__(self):
        super().__init__()

signal_manager = AccelerationSignalManager()  # Create a global signal manager