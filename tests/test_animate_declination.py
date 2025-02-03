# Testing animate_declination() method from compass.py

import pytest

from dmcview.compass import Compass


@pytest.fixture
def compass(qtbot):
    widget = Compass()
    qtbot.addWidget(widget)
    return widget


def test_animate_declination(compass):
    
    compass.current_declination= 0
    compass.target_declination = 45.55
    compass.__animate_declination()

    assert compass.current_declination != 0
