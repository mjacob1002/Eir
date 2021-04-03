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

class ProbabilityExcpetion(Exception):
    """Makes sure that values are between 0 and 1, inclusive."""
    def __init__(self, *args):
        super().__init__()
        if args:
            self.message = args[0]
            # determines whether the probability is greater than 1 or less than 0
            self.tooBig = True
        else:
            self.message = None
    
    def __str__(self):
        if self.tooBig:
            return f"{self.message} > 1, which is too big for a probability."
        else:
            return f"{self.message} < 0, which is to small for a probability"
    

        