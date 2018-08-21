from .constants import *


class Change:
    def __init__ (self, stage, sequence):
        self.stage = stage
        self.sequence = sequence
    
    def transpose (self, transposition):
        return Change (self.stage, [self.sequence [transposition [i]] for i in range (self.stage)])
    
    def clone (self):
        return Change (self.stage, self.sequence [:])
    
    def order (self):
        change = self
        iterations = 2
        while iterations < 1000:
            change = change.transpose (self.sequence)
            if change.sequence == rounds (self.stage).sequence:
                return iterations
            iterations += 1
    
    def get_bell_sets (self):
        sets = []
        bells_so_far = []
        
        for i in range (self.stage):
            if not i in bells_so_far:
                bells_so_far.append (i)
                
                iterations = 0
                change = self
                current_set = [i]
                while iterations < 50:
                    new_place_bell = change.sequence.index (i)
                    
                    if new_place_bell == i:
                        break
                        
                    bells_so_far.append (new_place_bell)
                    current_set.append (new_place_bell)
                        
                    change = change.transpose (self.sequence)
                    iterations += 1
                
                sets.append (current_set)
        
        return sets
                    
    
    def __str__ (self):
        string = ""
        for i in self.sequence:
            string += bell_names [i]
        return string
    
    def __repr__ (self):
        return self.__str__ ()
    
    def __getitem__ (self, item):
        return self.sequence [item]
    
    def __len__ (self):
        return self.stage
    
    def index (self, bell):
        return self.sequence.index (bell)


def rounds (stage):
    # type: (int) -> Change
    return Change (stage, [i for i in range (stage)])
