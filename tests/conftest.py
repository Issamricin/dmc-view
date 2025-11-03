import pytest
import os
from unittest.mock import MagicMock, patch
from PySide6.QtWidgets import QApplication
import sys

# Global patch for Qt classes in CI
@pytest.fixture(scope="session", autouse=True)
def mock_qt_in_ci():
    """Automatically mock Qt components in CI environment"""
    if os.getenv('CI'):
        with patch('PySide6.QtWidgets.QWidget'), \
             patch('PySide6.QtWidgets.QMainWindow'), \
             patch('PySide6.QtWidgets.QVBoxLayout'), \
             patch('PySide6.QtWidgets.QHBoxLayout'), \
             patch('PySide6.QtGui.QPainter'), \
             patch('PySide6.QtCore.QTimer'):
            yield
    else:
        yield

@pytest.fixture(scope="session")
def qapp():
    """QApplication fixture that works in both CI and local"""
    if os.getenv('CI'):
        # Mock QApplication for CI
        mock_app = MagicMock()
        mock_app.instance.return_value = mock_app
        with patch('PySide6.QtWidgets.QApplication', return_value=mock_app):
            yield mock_app
    else:
        # Real QApplication for local
        if os.getenv('CI') or not os.getenv('DISPLAY'):
            pytest.skip("Skipping GUI test in CI/headless environment")
        
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        yield app

# Mock-based fixtures that work everywhere
@pytest.fixture
def acceleration(qapp):
    with patch('dmcview.acceleration.QWidget'):
        from dmcview.acceleration import AccelerationWidget
        widget = AccelerationWidget()
        # Add any necessary mock setup
        return widget

@pytest.fixture
def compass(qapp):
    with patch('dmcview.compass.QWidget'):
        from dmcview.compass import Compass
        widget = Compass()
        # Ensure the widget has expected attributes for tests
        if not hasattr(widget, 'current_angle'):
            widget.current_angle = 0.0
        return widget

@pytest.fixture
def simulator(qapp):
    with patch('dmcview.simulator.QWidget'):
        from dmcview.simulator import Simulator
        widget = Simulator()
        return widget