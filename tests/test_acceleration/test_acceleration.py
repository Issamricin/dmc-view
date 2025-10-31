import pytest
from unittest.mock import MagicMock, patch
import numpy as np

from dmcview.acceleration import Accelaration3D


@pytest.fixture
def mock_signal_manager(monkeypatch):
    """Mock the signal manager to track emitted values."""
    mock_signal = MagicMock()
    monkeypatch.setattr("dmcview.acceleration.signal_manager.data_signal", mock_signal)
    return mock_signal

@pytest.fixture
def accel(mock_signal_manager, monkeypatch):
    monkeypatch.setattr("dmcview.acceleration.QTimer", MagicMock())
    monkeypatch.setattr("dmcview.acceleration.Figure", MagicMock())
    instance = Accelaration3D()
    instance.ax = MagicMock()
    instance.ax.quiver.return_value = MagicMock()
    instance.draw = MagicMock()
    instance.quiver = MagicMock()
    return instance

def test_update_acceleration_rounding(accel):
    accel.update_acceleration(1.1, 2.3, 4.5)

    assert accel.x == 1.0
    assert accel.y == 2.2
    assert accel.z == 4.4


def test_update_acceleration_vector_positive(accel, mock_signal_manager):
    """Verify update_acceleration_vector emits correct values and updates quiver."""
    accel.x, accel.y, accel.z = 2.0, 3.0, 4.0
    accel.target_x, accel.target_y, accel.target_z = 0.0, 0.0, 0.0
    accel.value = 0.2

    accel.ax.quiver.return_value = MagicMock()
    accel.quiver = MagicMock()

    accel.update_acceleration_vector()

    # The target values should move towards x,y,z by value=0.2
    assert accel.target_x > 0
    assert accel.target_y > 0
    assert accel.target_z > 0

    # The signal was emitted with rounded floats
    mock_signal_manager.emit.assert_called()
    args = mock_signal_manager.emit.call_args[0]
    assert len(args) == 3
    assert all(isinstance(v, float) for v in args)

    accel.draw.assert_called_once()



def test_update_acceleration_vector_negative(accel, mock_signal_manager):
    """Verify update_acceleration_vector emits correct values and updates quiver."""
    accel.x, accel.y, accel.z = 0.0, 0.0, 0.0
    accel.target_x, accel.target_y, accel.target_z = 2.0, 4.0, 5.5
    accel.value = 0.2

    accel.ax.quiver.return_value = MagicMock()
    accel.quiver = MagicMock()

    accel.update_acceleration_vector()

    # The target values should move towards x,y,z by value=0.2
    assert accel.target_x != 2.0
    assert accel.target_y != 4.0
    assert accel.target_z != 5.5

    # The signal was emitted with rounded floats
    mock_signal_manager.emit.assert_called()
    args = mock_signal_manager.emit.call_args[0]
    assert len(args) == 3
    assert all(isinstance(v, float) for v in args)

    accel.draw.assert_called_once()
