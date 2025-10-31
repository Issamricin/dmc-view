from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest

from dmcview.cli import start_input


@pytest.fixture
def fake_args():
    """Return args namespace with all fields None (forcing input mode)."""
    return SimpleNamespace(a=None, d=None, b=None, e=None, ac=None)


@patch("dmcview.cli.QApplication")  # prevent real app window
@patch("dmcview.cli.QWidget")
@patch("dmcview.cli.QHBoxLayout")
@patch("dmcview.cli.Accelaration3D")
@patch("dmcview.cli.Compass")
@patch("dmcview.cli.get_float_input")
@patch("dmcview.cli.get_acceleration_input")
def test_start_input_with_mocked_ui(
    mock_acc_input,
    mock_float_input,
    MockCompass,
    MockAccel,
    _MockLayout,
    _MockWidget,
    MockApp,
    fake_args,
):
    """Test start_input() safely without opening GUI."""
    # Arrange
    mock_float_input.side_effect = [45.5, 30.0, 5.0, 20.0]  # simulate numeric inputs
    mock_acc_input.return_value = (1.0, 2.0, 3.0)

    mock_app_instance = MagicMock()
    MockApp.return_value = mock_app_instance

    compass_instance = MagicMock()
    MockCompass.return_value = compass_instance

    accel_instance = MagicMock()
    MockAccel.return_value = accel_instance

    # Act
    start_input(fake_args)

    # Assert — check the right functions were called
    mock_float_input.assert_called()  # ensures it asked for user input
    mock_acc_input.assert_called_once()

    compass_instance.update_declination.assert_called_with(30.0)
    compass_instance.update_angle.assert_called_with(45.5)
    compass_instance.set_rotation.assert_called_with(5.0)
    compass_instance.set_elevation.assert_called_with(20.0)
    accel_instance.update_acceleration.assert_called_with(1.0, 2.0, 3.0)

    mock_app_instance.exec.assert_called_once()  # app started
