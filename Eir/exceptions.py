class NegativeValException(Exception):
    """Makes sure that values are non-negative."""
    
    def __init__(self, *args):
        super().__init__()
        if args:
            self.message = args[0]
        else:
            self.message = None
    
    def __str__(self):
        if self.message:
            return f"{self.message} is negative when no negative values are allowed."
        else:
            return "NegativeValException was raised."

class ProbabilityException(Exception):
    """Makes sure that values are between 0 and 1, inclusive."""
    def __init__(self, *args):
        super().__init__()
        if args:
            self.message = args[0]
            # determines whether the probability is greater than 1 or less than 0
            self.tooBig = args[1]
        else:
            self.message = None
    
    def __str__(self):
        if self.tooBig:
            return f"{self.message} > 1, which is too big for a probability."
        else:
            return f"{self.message} < 0, which is to small for a probability"

class NotIntException(Exception):
    """Checks to make sure that an int passed in to the parameter."""

    def __init__(self, *args):
        super().__init__()
        if args:
            self.message = args[0]
        else:
            self.message = None
    
    def __str__(self):
        if self.message:
            return f"{self.message} is supposed to be an integer."
        else:
            return "NotIntException was raised."

class NotFloatException(Exception):
    """Checks to make sure an int/float was passed in as a parameter."""
    def __init__(self, *args):
        super().__init__()
        if args:
            self.message = args[0]
        else:
            self.message = None
    
    def __str__(self):
        if self.message:
            return f"{self.message} is not a number. Please enter a non-negative number."
        else:
            return "NotFloatException was raised."

class DayOutOfRange(Exception):
    """ Checks to make sure that the day inputted in any Simul_Details is in the range of 0, self.days+1"""

    def __init__(self, *args):
        super().__init__()
        if args:
            self.message = args[0]
        else:
            self.message = None
        
    def __str__(self):
        if self.message:
            return f"Days only go from 0 to {self.days}; {self.message} is out of range."
        else:
            return "DayOutOfRange Exception"

class PersonNotFound(Exception):
    """ Thrown if the Person is not in the number of people in the simulation for the Simul_Details object."""

    def __init__(self, *args):
        super().__init__()
        if args:
            self.message = args[0]
        else:
            args = None
    
    def __str__(self):
        if self.message:
            return f"{self.message} is not found. Persons range from 0 to {self.popsize-1}."
        else:
            return "PersonNotFound Exception"
    

        