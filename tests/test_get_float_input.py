
from dmcview.cli import get_float_input


def test_get_float_input_with_valid_input(monkeypatch):
    monkeypatch.setattr('builtins.input',lambda _: "42.5")
    result = get_float_input("Enter the azimuth angle in degrees; for example 40.45",0.0)
    assert result == 42.5



def test_get_float_input_with_default(monkeypatch):

    monkeypatch.setattr('builtins.input',lambda _: "")
    result = get_float_input("Enter the azimuth angle in degrees; for example 40.45",0.0) 
    assert result == 0.0 #default


def test_get_input_with_invalid_then_valid_input(capsys, monkeypatch):
    
    inputs = iter(["abs","10.5"])
    monkeypatch.setattr('builtins.input',lambda _: next(inputs))

    result = get_float_input("Enter the azimuth angle in degrees; for example 40.45",0.0)
    captured = capsys.readouterr() #captures what was printed during the function call

    assert "Invalid input. Please enter a numeric value." in captured.out #check if this was printed correctly
    assert result == 10.5 
