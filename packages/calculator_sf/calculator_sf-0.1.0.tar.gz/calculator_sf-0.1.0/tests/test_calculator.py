from calculator_sf.calculator import Calculator

def test_calculator_add():
    calculator = Calculator()
    calculator.add(10)
    assert calculator.memory == 10
    
def test_calculator_subtract():
    calculator = Calculator()
    calculator.subtract(10)
    assert calculator.memory == -10
    
def test_calculator_multiply():
    calculator = Calculator(memory = 3)
    calculator.multiply(10)
    assert calculator.memory == 30

def test_calculator_divide():
    calculator = Calculator(memory = 10)
    calculator.divide(10)
    assert calculator.memory == 1

def test_calculator_n_root():
    calculator = Calculator(memory = 100)
    calculator.n_root(2)
    assert calculator.memory == 10

def test_calculator_reset():
    calculator = Calculator(memory = 50)
    calculator.reset()
    assert calculator.memory == 0