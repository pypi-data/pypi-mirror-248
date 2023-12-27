"""Calculator

This script contains a calculator framework that allows the user
to perform any arythmetic operations (addition, subtraction,
division and multiplication) and the nth root. The result is 
stored and automatically used as the left operand of the 
following operation.

"""

from typing import NamedTuple, List

Operation = NamedTuple('Operation', [('left_operand', float), 
    ('operation', str), ('right_operand', float),
    ('equal', str), ('result', float)])

class Calculator:
    """  
    The following class represents a calculator, it helps storing a number in
    memory and performing several algebraic operation

    Attributes
    ----------
    number : float
        a float which is the result of the last
        operation
    history : List[Operation]
        a list of all the numbers, operations,
        that were entered in the calculator
    width : int=4
        specifies the number of characters displayed
    precision : int=2
        indicates the number of characters used after the decimal point

    Methods
    -------
    add(number_to_add: float)
        Performs the addition betwen the number stored in the calculator and
        the one entered as an argument
        Prints the result
    subtract(subtrahend: float)
        Performs the subtraction betwen the number stored in the calculator
        and the one entered as an argument
        Prints the result
    multiply(multiplicand: float)
        Performs the multiplication betwen the number stored in the
        calculator and the multiplicand (argument)
        Prints the result
    divide(denominator: float)
        Performs the division betwen the number stored in the calculator
        (numerator) and the one entered as an argument (denominator)
        Prints the result
    nth_root(n: float)
        Performs the nth root of the number stored in the calculator
        Prints the result
    reset()
        Resets the calculator which returns to zero.
        Delete its history
    print_history()
        Prints the full history (all results, operands,
        and operations) of the calculator

    """

    def __init__(self, number: float=0, width: int=7, 
            precision: int=3) -> None:
        """
        Parameter
        ---------
        number : float=0
            If the user wants to intialize the calculator to a specific number
        width : int=4
            specifies the number of characters displayed
        precision : int=2
            indicates the number of characters used after the decimal point

        """
        self.number = number
        self.width = width
        self.precision = precision
        self.history: List[Operation] = []
        print(f'Calculator has been initialized to {self.number}.')

    def __str__(self):
        """
            Prints the number stored in the calculator
        """
        return f'res = {self.number:<{self.width}.{self.precision}f}'

    def add(self, number_to_add: float=0) -> float:
        """
        Performs the following addition
            number = number + number_to_add
        The result is then printed

        Parameter
        ---------
        number_to_add : float=0

        For example:

            >>> cal = Calculator()
            Calculator has been initialized to 0.
            >>> cal.add(2)
            2.000  
            >>> cal.add(7)
            9.000  

        """
        number_before = self.number
        self.number += number_to_add
        self.history.append(Operation(number_before, '+', 
            number_to_add, '=', self.number))
        print(f'{self.number:<{self.width}.{self.precision}f}')
        return self.number;

    def subtract(self, subtrahend: float=0) -> float:
        """
        Performs the following sustraction
            number = number - subtrahend
        The result is then printed

        Parameter
        ---------
        subtrahend : float=0

        For example:

            >>> cal = Calculator()
            Calculator has been initialized to 0.
            >>> cal.subtract(8)
            -8.000 
            >>> cal.subtract(-17.3)
            9.300  
        """
        number_before = self.number
        self.number -= subtrahend
        self.history.append(Operation(number_before, '-', 
            subtrahend, '=', self.number))
        print(f'{self.number:<{self.width}.{self.precision}f}')
        return self.number;

    def multiply(self, multiplicand: float=1) -> float:
        """
        Performs the following multiplication
            number = number * multiplicand
        The result is then printed

        Parameter
        ---------
        number_to_multiply : float=1

        For example:

            >>> cal = Calculator()
            Calculator has been initialized to 0.
            >>> cal.add(6.2)
            6.200  
            >>> cal.multiply(-19.41)
            -120.342

        """
        number_before = self.number
        self.number *= multiplicand
        self.history.append(Operation(number_before, '*', 
            multiplicand, '=', self.number))
        print(f'{self.number:<{self.width}.{self.precision}f}')
        return self.number;

    def divide(self, denominator: float=1) -> float:
        """
        Performs the following division
            number = number / denominator
        The result is then printed

        Parameter
        ---------
        denominator : float=1

        For example:

            >>> cal = Calculator()
            Calculator has been initialized to 0.
            >>> cal.add(2.3)
            2.300  
            >>> cal.divide(-4.5)
            -0.511 
        """
        #Validation to prevent from dividing by zero
        assert denominator != 0, 'The denominator cannot be 0!'
        number_before = self.number
        self.number /= denominator
        self.history.append(Operation(number_before, '/',
            denominator, '=', self.number))
        print(f'{self.number:<{self.width}.{self.precision}f}')
        return self.number;

    def nth_root(self, n: float) -> float:
        """
        Performs the following nth root (not restricted to integer)
            number = number ** (1 / n)
        n must be striclty positive
        The result is then printed

        Parameter
        ---------
        denominator : float=1

        For example:

            >>> cal = Calculator()
            Calculator has been initialized to 0.
            >>> cal.add(12.1)
            12.100 
            >>> cal.nth_root(1.5)
            5.271  
        """
        #Validation for the nth root operand
        assert n > 0, f'The nth_root operand {n} must be strictly positive!'
        assert self.number > 0, 'The radican must be positive!'
        number_before = self.number
        self.number  = self.number ** (1 / n)
        self.history.append(Operation(number_before, 'r', n, '=', self.number))
        print(f'{self.number:<{self.width}.{self.precision}f}')
        return self.number;

    def reset(self) -> None:
        """
        Resets the calculator to 0 and deletes its history.
        """
        self.number = 0
        self.history = []
        print('Calculator has been resetted')

    def print_history(self) -> None:
        """
        Prints the calculator's history. 
        """
        for i in self.history: 
            print(' '.join([f'{getattr(i, j):^{2*self.width}.{self.precision}f}'
                if type(getattr(i,j))!=str else f'{getattr(i,j): ^{self.width}}'
                for j in Operation._fields]))
