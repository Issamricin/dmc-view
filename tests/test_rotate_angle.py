# Testing rotate_angle() method from compass.py

import pytest

from dmcview.compass import Compass


@pytest.fixture
def compass(qtbot):  # qtbot is provided by pytest-qt
    widget = Compass()
    qtbot.addWidget(widget)
    return widget


def test_rotate_angle(compass):

    compass.current_angle = 0
    compass.target_angle = 5

    compass._Compass__rotate_angle()
    assert compass.current_angle != 0
