from PySide6.QtCore import QObject, Signal

class SignalManager(QObject):
    data_signal = Signal(float, float, float)  # Signal that sends three float values (x, y, z)

    def __init__(self):
        super().__init__()

signal_manager = SignalManager()  # Create a global signal manager