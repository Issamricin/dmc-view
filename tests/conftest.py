import pytest
import os
from PySide6.QtWidgets import QApplication
import sys

@pytest.fixture(scope="session")
def qapp():
    """QApplication fixture that only runs if display is available"""
    if os.getenv('CI') or not os.getenv('DISPLAY'):
        pytest.skip("Skipping GUI test in CI/headless environment")
    
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    yield app