class Calculator:
    """Create a Calculator class object.

    The Calculator class represents a basic calculator with memory storage. The memory starts at a default 
    value of 0.0 but can be updated using various functions.

    Parameters:
        memory (float, optional): The initial value for the calculator memory. Defaults to 0.0.

    Example:
        >>> calculator = Calculator()  # Creates a calculator with default memory (0.0)
        >>> calculator = Calculator(memory=5.0)  # Creates a calculator with initial memory set to 5.0
    """
    def __init__(self, memory: float=0.0, decimal_places: int = 3):
        """Initialize a new Calculator object with optional initial memory and decimal places.

        Parameters:
            memory (float, optional): The initial value for the calculator memory. Defaults to 0.0.
            decimal_places (int, optional): The number of decimal places to round results to. Defaults to 
            3.
        """
        self._memory = memory
        self._decimal_places = decimal_places
        
    def get_memory(self) -> float:
        """Get the current value stored in the calculator memory.
        
        This method retrieves the current numeric value stored in the calculator's memory. The memory 
        serves as a temporary storage location for numerical results obtained through various calculator 
        operations. Calling this method allows external code to access and retrieve the current content of 
        the calculator's memory.

        Returns:
            float: The current numeric value stored in the calculator memory.

        Example:
            To obtain the current value stored in the calculator memory:
            >>> current_memory = calculator.get_memory()
        """
        return self._memory

    def get_decimal_places(self) -> int:
        """Get the current number of decimal places used for rounding in the calculator.

        This method retrieves the current setting for the number of decimal places used in rounding
        results within the calculator. The decimal places setting determines the precision of numerical 
        results displayed or stored by the calculator's operations. Calling this method allows external 
        code to access and retrieve the current decimal places setting. The default value is 3.

        Parameters:
            None
        
        Raises:
            No specific exceptions are raised by this method.

        Returns:
            int: The current number of decimal places used for rounding.

        Example:
            To obtain the current number of decimal places for rounding:
            >>> current_decimal_places = calculator.get_decimal_places()
        """
        return self._decimal_places
        
    def _round_result(self, result: float) -> float:
        """
        Round a floating-point number to the specified decimal places.

        Parameters:
            result (float): The floating-point number to be rounded.
            
        Raises:
            ValueError: If the result is not a valid floating-point number.

        Returns:
            float: The rounded result with the specified number of decimal places. This has a default 
            value of 3 which can be edited in the class attribute decimal_places.
        
        Example:
            To round a result to the default of 3 decimal places:
            >>> calculator = Calculator()
            >>> rounded_result = calculator._round_result(5.678)
            >>> print(rounded_result)
            5.678

            To round a result to a different number of decimal places:
            >>> calculator = Calculator(decimal_places=2)
            >>> rounded_result = calculator._round_result(5.678)
            >>> print(rounded_result)
            5.68
        """
        return round(result, self._decimal_places)

    def _validate_argument(self, x):
        """
        Validate the input argument to ensure it is either an integer or a float.

        This method checks if the provided argument `x` is of valid type, which should be either an 
        integer or a float. If the input is not of the expected types, a TypeError is raised with a 
        detailed error message indicating the expected types.

        Parameters:
            x (int or float): The input value to be validated.

        Raises:
            TypeError: If the input `x` is not of type int or float.
            
        Returns:
            None

        Example:
            To validate an argument before performing a calculation:
            >>> self._validate_argument(3.14)
        """
        valid_types = (int, float)
        if not isinstance(x, valid_types):
            raise TypeError(f"Invalid argument type. Expected {valid_types}, got {type(x).__name__}")

    
    def add(self, x: float):
        """Add a value to the calculator memory.

        This method adds the specified value `x` to the current memory value.
        
        Parameters:
            x (float): The value to be added to the memory.

        Raises:
            ValueError: If the input `x` is not a valid float.
            
        Returns:
            float: The updated value in the calculator memory after adding `x`.

        Example:
            To add 5.0 to the memory:
            >>> calculator.add(5.0)
        """
        self._validate_argument(x)
        result = self._memory + x
        self._memory = self._round_result(result)
        return self._memory

    def subtract(self, x: float):
        """Subtract a value from the calculator memory.

        This method subtracts the specified value `x` from the current memory value.
        
        Parameters:
            x (float): The value to be subtracted from the memory.

        Raises:
            ValueError: If the input `x` is not a valid float.
        
        Returns:
            float: The updated value in the calculator memory after subtracting `x`.

        Example:
            To subtract 5.0 from the memory:
            >>> calculator.subtract(5.0)
        """
        self._validate_argument(x)
        result = self._memory - x
        self._memory = self._round_result(result)
        return self._memory
    
    def multiply(self, x: float):
        """Multiply the calculator memory by a specified value.

        This method multiplies the current value in the calculator memory by the specified value `x`. The 
        result becomes the new value in the calculator memory.

        Parameters:
            x (float): The value to multiply the memory by.

        Raises:
            ValueError: If the input `x` is not a valid float.
        
        Returns:
            float: The updated value in the calculator memory after multiplying by `x`.

        Example:
            To multiply the memory by 3.0:
            >>> calculator.multiply(3.0)
        """
        self._validate_argument(x)
        result = self._memory * x
        self._memory = self._round_result(result)
        return self._memory
    
    def divide(self, x: float):
        """Divide the calculator memory by a specified value.

        This method divides the current value in the calculator memory by the specified value `x`. The 
        result becomes the new value in the calculator memory.

        Parameters:
            x (float): The value to divide the memory by.

        Raises:
            ValueError: If the input `x` is not a valid float.
            ZeroDivisionError: If the input `x` is zero.
            
        Returns:
            float: The updated value in the calculator memory after dividing by `x`.

        Example:
            To divide the memory by 2.0:
            >>> calculator.divide(2.0)
        """
        self._validate_argument(x)
        if x != 0:
            result = self._memory / x
            self._memory = self._round_result(result)
        else:
            raise ValueError("Cannot divide by 0. Please choose another number.")
        return self._memory
    
    def n_root(self, n: int):
        """Calculate the Nth root of the calculator memory.

        This method raises the current value in the calculator memory to the power of 1/N, where N is the 
        specified integer `n`. The result becomes the new value in the calculator memory.

        Parameters:
            n (int): The exponent for the Nth root.

        Raises:
            ValueError: If the input `n` is not a valid integer.
            ValueError: If the input `n` is less than or equal to 0.
            
        Returns:
            float: The updated value in the calculator memory after taking the `x` root.

        Example:
            To calculate the square root of the memory:
            >>> calculator.n_root(2)
        """
        self._validate_argument(x)
        if n > 0:
            result = self._memory ** (1/n)
            self._memory = self._round_result(result)
        else:
            raise ValueError("Cannot take the 0th or negative root. Please choose another number.")
        return self._memory
    
    def reset(self):
        """Reset the calculator memory.

        This method sets the calculator memory to its initial state, which is 0.0.

        Parameters:
            None
        
        Returns:
            float: 0.0, the reset calculator memory.

        Example:
            To reset the calculator memory:
            >>> calculator.reset()
        """
        self._memory = 0.0
        return self._memory