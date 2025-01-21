# test_compass_drawings.py

from unittest.mock import MagicMock

import pytest
from PySide6.QtCore import QPointF

from dmcview.compass import Compass


@pytest.fixture
def compass(qtbot):
    widget = Compass()
    qtbot.addWidget(widget)
    return widget

@pytest.fixture
def painter():
    return MagicMock()

def test_draw_cardinal_points(compass, painter):
    compass.draw_cardinal_points(painter, QPointF(100, 100), 50)
    assert painter.drawText.call_count == 4  # for N, W, E, S

def test_draw_lines(compass, painter):
    compass.draw_lines(painter, QPointF(100, 100), 50)
    assert painter.drawLine.call_count > 0

def test_draw_arrow(compass, painter):
    compass.current_angle = 45
    compass.draw_arrow(painter, QPointF(100, 100), 50)
    assert painter.drawPolygon.called

def test_draw_rotating_magnetic_north(compass, painter):
    compass.draw_rotating_magnetic_north(painter, QPointF(100, 100), 50, 0, 10)
    assert painter.drawPolygon.called

def test_draw_red_line(compass, painter):
    compass.draw_red_line(painter, QPointF(100, 100), 10)
    assert painter.drawLine.call_count == 1
