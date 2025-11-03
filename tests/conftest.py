import pytest
import os
from PySide6.QtWidgets import QApplication
import sys

@pytest.fixture(scope="session")
def qapp():
    if os.getenv('CI') or not os.getenv('DISPLAY'):
        pytest.skip("Skipping GUI test in CI/headless environment")
    
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    yield app

@pytest.fixture
def compass(qapp):  # This will auto-skip in CI due to qapp dependency
    from dmcview.compass import Compass
    return Compass()

def pytest_collection_modifyitems(config, items):
    """Skip compass tests in CI at collection time"""
    if os.getenv('CI'):
        skip_gui = pytest.mark.skip(reason="GUI test skipped in CI")
        for item in items:
            if "compass" in item.nodeid:
                item.add_marker(skip_gui)