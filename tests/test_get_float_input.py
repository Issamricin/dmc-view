import sys
sys.path[0]='/home/python/Desktop/DMC_project/dmc-view/src/dmc_view' # was facing ModuleNotFoundError so this fixed it 

import pytest
from src.dmc_view.main import get_float_input


def test_get_float_input_with_valid_input(monkeypatch):

    monkeypatch.setattr('builtins.input',lambda _: "42.5")
    result = get_float_input("Enter the azimuth angle in degrees; for example 40.45",0.0)
    assert result == 42.5



def test_get_float_input_with_default(monkeypatch):

    monkeypatch.setattr('builtins.input',lambda _: "")
    result = get_float_input("Enter the azimuth angle in degrees; for example 40.45",0.0) 
    assert result == 0.0