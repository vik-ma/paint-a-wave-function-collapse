class RuleIndex:
    """
    This is a class to store the rules for adjacent tiles in the wave function collapse algorithm.

    Attributes:
        data (dict): A dictionary that stores a list of patterns that are allowed at every relative position at current index.
    
    Methods:
        add_rule(self, pattern, relative_position, next_pattern)
            Adds next_pattern to the list of allowed patterns at relative postion of the current index.
        check_possibility(self, pattern, check_pattern, relative_position)
            Returns True if check_pattern is in stored list of allowed patterns, otherwise False.
    """
    def __init__(self, pattern_list, directions):
        self.data = {}
        for pattern in pattern_list:
            self.data[pattern] = {}
            for direction in directions: 
                self.data[pattern][direction] = []
    
    def add_rule(self, pattern, relative_position, next_pattern):
        self.data[pattern][relative_position].append(next_pattern)
        
    def check_possibility(self, pattern, check_pattern, relative_position):
        if isinstance(pattern, list):
            pattern = pattern[0]

        return check_pattern in self.data[pattern][relative_position]