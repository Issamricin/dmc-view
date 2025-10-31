import pytest
from unittest.mock import patch, MagicMock
from PySide6.QtWidgets import QApplication
from dmcview.simulator import SimulatorRunner, Simulator


@pytest.fixture
def simulator():

    with patch.object(Simulator, 'thread_pool', create=True), \
         patch.object(SimulatorRunner, 'run', lambda self: None):
        sim = Simulator()

        # Patch GUI-heavy methods to avoid drawing
        sim.compass.paintEvent = MagicMock()
        sim.compass.create_static_pixmap = MagicMock()
        sim.compass.start_animation_timer = MagicMock()
        sim.canvas.update_acceleration = MagicMock()

        yield sim

def test_runner_stop():
    runner = SimulatorRunner()
    assert runner.running is True
    runner.stop()
    assert runner.running is False

def test_update_method(simulator):
    # Patch compass and canvas methods to track calls
    simulator.compass.update_angle = MagicMock()
    simulator.compass.set_elevation = MagicMock()
    simulator.compass.set_rotation = MagicMock()
    simulator.canvas.update_acceleration = MagicMock()

    # Call the private update method directly
    simulator._Simulator__update("30", "25", "40", "10", "10", "0")

    simulator.compass.update_angle.assert_called_with(30.0)
    simulator.compass.set_elevation.assert_called_with(25.0)
    simulator.compass.set_rotation.assert_called_with(40.0)
    simulator.canvas.update_acceleration.assert_called_with(10.0, 10.0, 0.0)

def test_runner_run_once(monkeypatch):
    runner = SimulatorRunner()

    # Patch QThread.sleep to skip delay
    monkeypatch.setattr("PySide6.QtCore.QThread.sleep", lambda x: None)

    # Attach mock to signal
    mock_slot = MagicMock()
    runner.signal.result.connect(mock_slot)

    # Make it run exactly one iteration
    def stop_after_one_emit(*args, **kwargs):
        runner.running = False
    runner.signal.result.connect(stop_after_one_emit)

    # Start with running=True
    runner.running = True

    runner.run()

    # The mock should have been called once
    mock_slot.assert_called_once()
