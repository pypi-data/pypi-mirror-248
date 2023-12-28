import pytest
from calculator_sf.calculator import Calculator
from itertools import product

def test_calculator_add():
    calculator = Calculator()
    calculator.add(10)
    assert calculator._memory == 10
    
def test_calculator_subtract():
    calculator = Calculator()
    calculator.subtract(10)
    assert calculator._memory == -10
    
def test_calculator_multiply():
    calculator = Calculator(memory = 3)
    calculator.multiply(10)
    assert calculator._memory == 30

def test_calculator_divide():
    calculator = Calculator(memory = 10)
    calculator.divide(10)
    assert calculator._memory == 1

def test_calculator_reset():
    calculator = Calculator(memory = 50)
    calculator.reset()
    assert calculator._memory == 0

@pytest.mark.parametrize("memory, inputs, expected_result", [
    (0.0, [(2.0, 'add'), (3.0, 'multiply'), (4.0, 'subtract')], 2.0),
    (5.0, [(2.0, 'divide'), (0.0, 'add')], 2.5),
    # Add more test cases as needed
])
def test_calculator_operations(memory, inputs, expected_result):
    calculator = Calculator(memory=memory)
    for value, operation in inputs:
        getattr(calculator, operation)(value)
    assert calculator.get_memory() == expected_result

@pytest.mark.parametrize("memory, n, expected_result", [
    (4.0, 2, 2.0),
    (8.0, 3, 2.0),
    # Add more test cases as needed
])
def test_calculator_n_root(memory, n, expected_result):
    calculator = Calculator(memory=memory)
    calculator.n_root(n)
    assert calculator.get_memory() == expected_result
