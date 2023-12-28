import pytest
from dscalculator.calculator import Calculator

def test_add_mltpl():
    calcul = Calculator()
    assert calcul.memorised_value == 0.0
    assert calcul.add(3, 2, 5) == 10.0
    assert calcul.memorised_value == 10.0
    
def test_add_single():
    calcul = Calculator()
    assert calcul.add(9) == 9.0
    assert calcul.memorised_value == 9.0
    
def test_add_chain():
    calcul = Calculator()
    assert calcul.memorised_value == 0.0
    assert calcul.add(3, 2, 5) == 10.0
    assert calcul.memorised_value == 10.0
    assert calcul.add(1, 4) == 15.0
    assert calcul.memorised_value == 15.0

def test_subtract():
    calcul = Calculator()
    assert calcul.subtract(3, 2) == -5.0
    assert calcul.memorised_value == -5.0

def test_multiply_from_starting():
    calcul = Calculator()
    assert calcul.multiply(2) == 0.0
    assert calcul.memorised_value == 0.0
    
def test_multiply():
    calcul = Calculator()
    calcul.add(9)
    assert calcul.multiply(3) == 27.0
    assert calcul.memorised_value == 27.0
    
def test_multiply_chain():
    calcul = Calculator()
    calcul.add(9)
    assert calcul.multiply(3) == 27.0
    assert calcul.memorised_value == 27.0
    assert calcul.multiply(2) == 54.0
    assert calcul.memorised_value == 54.0

def test_divide():
    calcul = Calculator()
    calcul.add(25.0)
    assert calcul.divide(5) == 5.0
    assert calcul.memorised_value == 5.0
    with pytest.raises(ValueError):
        calcul.divide(0)

def test_root_n():
    calcul = Calculator()
    calcul.add(64)
    assert calcul.root_n(2) == 8.0
    with pytest.raises(ValueError):
        calcul.root_n(-1)

def test_reset():
    calcul = Calculator()
    calcul.add(100)
    calcul.reset()
    assert calcul.memorised_value == 0.0