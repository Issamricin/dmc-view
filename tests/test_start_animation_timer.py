# Test for start_animation_timer() method in compass.py

import pytest

from dmcview.compass import Compass


@pytest.fixture
def compass(qtbot):  # qtbot is provided by pytest-qt
    widget = Compass()
    qtbot.addWidget(widget)
    return widget



def test_start_animation_timer(compass):

    compass.start_animation_timer()
    assert compass.azimuth_timer.isActive()
    assert compass.declination_timer.isActive()
