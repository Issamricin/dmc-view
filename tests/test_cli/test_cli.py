from unittest.mock import patch
import pytest
from dmcview import cli
import builtins

def test_main_starts_simulator(monkeypatch):
    # Patch simulator to prevent real GUI
    monkeypatch.setattr(cli, "start_simulator", lambda: print("simulator started"))

    test_args = ["dmcview", "-s", "Y"]
    with patch("sys.argv", test_args):
        cli.main()  # Should call start_simulator()

    # No assertion needed if it just runs without error, 
    # but you can also mock start_simulator to assert_called_once()


def test_get_float_input_valid(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "42.0")
    assert cli.get_float_input("Enter angle", 10.0) == 42.0

def test_get_float_input_default(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "")
    assert cli.get_float_input("Enter angle", 10.0) == 10.0


def test_get_acceleration_input(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "1.0 2.0 3.0")
    assert cli.get_acceleration_input("Enter the acceleration values(vectors: x,y,z); for example 12 12 13",
            5.0,
            2.3,
            5.0) == (1.0, 2.0, 3.0)

def test_get_acceleration_input_default(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "")
    assert cli.get_acceleration_input("Enter the acceleration values(vectors: x,y,z); for example 12 12 13",
            5.0,
            2.3,
            5.0) == (5.0, 2.3, 5.0)
    
def test_get_acceleration_input_invalid(monkeypatch, capsys):
    responses = iter(["a b c", "1 2 3"])

    monkeypatch.setattr("builtins.input", lambda _: next(responses))
    result = cli.get_acceleration_input("Enter the acceleration values(vectors: x,y,z); for example 12 12 13",
            5.0,
            2.3,
            5.0) 
    
    captured = capsys.readouterr()

    assert "Invalid input. Please enter a correct numeric value." in captured[0]

    assert result == (1, 2, 3)

