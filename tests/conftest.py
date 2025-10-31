# tests/conftest.py
import pytest
from unittest.mock import MagicMock, patch

@pytest.fixture(scope="session", autouse=True)
def mock_qapplication():
    """
    Mock QApplication globally so PySide6 code can be imported
    without requiring a display or graphics libraries.
    """
    with patch("PySide6.QtWidgets.QApplication", MagicMock()):
        yield
