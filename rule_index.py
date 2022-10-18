class RuleIndex:
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