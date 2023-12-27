import typing

class Calculator:
    """Create Calculator class.
    """
    def __init__(self, memory: float=0.0):
        """The calculator stores memory, beginning at value 0.0, that will be updated depending on 
        functions called.
        """
        self.memory = memory

    def add(self, x: float):
        """Addition function. Adds user input, x, to value of calculator memory.
        """
        self.memory += x

    def subtract(self, x: float):
        """Subtraction function. Subtracts user input, x, from value of calculator memory.
        """
        self.memory -= x
    
    def multiply(self, x: float):
        """Multiplication function. Multiplies user input, x, by value of calculator memory.
        """
        self.memory *= x
    
    def divide(self, x: float):
        """Division function. Divides value of calculator memory by user input, x.
        """
        if x != 0:
            self.memory /= x
    
    def n_root(self, n: int):
        """(N) root function. Raises value of calculator memory to user input, n.
        """
        if n != 0:
            self.memory = self.memory ** (1/n)
    
    def reset(self):
        """Reset memory function. Resets value of calculator memory to 0.0.
        """
        self.memory = 0.0