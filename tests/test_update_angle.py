
import pytest

from dmcview.compass import Compass


@pytest.fixture
def compass(qtbot):  # qtbot is provided by pytest-qt
    widget = Compass()
    qtbot.addWidget(widget)
    return widget

def test_update_angle(compass): # Azimuth angle

    compass.update_angle(45.55)
    assert compass.target_angle == 45.55

def test_update_declination(compass): # Declination angle

    compass.update_declination(45.55)
    assert compass.target_declination == 45.55
