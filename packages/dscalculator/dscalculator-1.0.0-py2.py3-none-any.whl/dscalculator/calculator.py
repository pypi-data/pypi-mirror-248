"""
This is the main module for the dscalculator package.
It includes a Calculator class to handle simple mathematical operations building
upon Calculator's memory value which, upon initialization, is equal to 0.
The supported operations are as follows:

- Addition / Subtraction of Calculator's memory value to 1 or more provided inputs;
- Multiplication / Division of Calculator's memory value to 1 or more provided inputs;
- Take (n) root of Calculator's memory value.

Calculator's memory value gets updated with any chain of operations. However,
this value can be reset to zero on-demand.

Providing a large number of inputs to Addition / Subtraction or Multiplication / Division
methods might result in failure to compute output values depending on available computational/memory resources.
"""

__version__= "1.0.0"

from typing import Union


class Calculator:
    """A basic calculator class that can perform simple mathematical operations.

    It memorises the result of the most recent operation and can build upon it.
    The memorised value can be reset to zero on-demand.
    Addition, subtraction, multiplication, division, and taking nth root is supported
    by calculator's different methods.

    Attributes:
        memorised_value (float): The memorised value that is used in the calculations.
    """
    memorised_value: float
    
    def __init__(self):
        """Initialize a Calculator object with its memory value as 0.0"""
        self.memorised_value = 0.0

    def add(self, *terms: Union[int, float]) -> float:
        """Add a 1 or more numbers to Calculator's memory. If no term is provided 
        as an argument, Calculator's memorised value will be returned.
        """
        self.memorised_value = sum((self.memorised_value,) + terms)
        return self.memorised_value
    
    def subtract(self, *terms: Union[int, float]) -> float:
        """Subtract 1 or more numbers from Calculator's memory. If no term is provided 
        as an argument, Calculator's memorised value will be returned.
        """
        self.memorised_value -= sum(terms)
        return self.memorised_value

    def multiply(self, *terms: Union[int, float]) -> float:
        """Multiply Calculator's memory by 1 or more numbers. If no term is provided 
        as an argument, Calculator's memorised value will be returned.
        """
        multiplication_base = 1.0
        for term in terms:
            multiplication_base *= term
        self.memorised_value *= multiplication_base
        return self.memorised_value
    
    def divide(self, *terms: Union[int, float]) -> float:
        """Divise Calculator's memory by 1 or more numbers. If no term is provided 
        as an argument, Calculator's memorised value will be returned.
        Raises:
            ValueError: If any of the provided inputs is 0.
        """
        if not terms:
            return self.memorised_value
        for term in terms:
            if term == 0:
                raise ValueError("Division by zero is not allowed.")
            self.memorised_value /= term
        return self.memorised_value
    
    def root_n(self, n: Union[int, float]) -> float:
        """Get the nth root of Calculator's memory value.
        Raises:
            ValueError: If Calculator's memory value is equal to zero or negative.
        """
        if n <= 0:
            raise ValueError("n - the degree of the root - is expected to be positive.")
        self.memorised_value **= (1/n)
        return self.memorised_value
    
    def reset(self):
        """Reset the Calculator's memory back to 0.0
        """
        self.memorised_value = 0.0

