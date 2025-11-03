import pytest
import os

def pytest_collection_modifyitems(config, items):
    """Skip ALL GUI tests in CI"""
    if os.getenv('CI'):
        skip_gui = pytest.mark.skip(reason="GUI tests skipped in CI")
        gui_files = ['test_acceleration', 'test_compass', 'test_simulator']
        
        for item in items:
            if any(gui_file in item.nodeid for gui_file in gui_files):
                item.add_marker(skip_gui)