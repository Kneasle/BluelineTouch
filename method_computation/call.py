import change, constants, utilities


class Call:
    def __init__ (self, name, place_notation, calling_positions = None, every = constants.EVERY_LEAD,
                  _from = constants.OVER_LEAD_HEAD):
        self.name = name
        self.place_notation = place_notation
        self.expanded_notation = utilities.full_notation_to_split_notation (self.place_notation)
        self.every = every
        self.from_ = _from
        self.calling_positions = calling_positions
        if self.from_ == constants.OVER_LEAD_HEAD:
            self.from_ = - (len (self.expanded_notation) - 1)
        
        self.lookup_table = None
        self.method = None
    
    def set_method (self, method):
        self.method = method
        
        if self.every == constants.EVERY_LEAD:
            self.every = method.lead_length
        
        self.lookup_table = utilities.generate_look_up_table (self.expanded_notation, self.method.stage)
    
    def __str__ (self):
        return self.name + ": " + str (self.place_notation) + " (every: " + str (self.every) + ", from: " + \
               str (self.from_) + ", calling positions: " + str (self.calling_positions) + ")"
    
    def __len__ (self):
        return len (self.expanded_notation)
    
    def __repr__ (self):
        return self.__str__ ()
    
    def compact_string (self):
        if self.every == constants.EVERY_LEAD:
            return self.name + "|" + self.place_notation + "|" + self.calling_positions
        else:
            return self.name + "|" + self.place_notation + "|" + str (self.calling_positions) + "|" + str (self.every) + \
                   "|" + str (self.from_)


def calls_from_string (string = "[B|14|IBFVXWH|48|0, S|14|23FVXWH|48|0]"):
    strings = string.strip ("[] ").replace (" ", "").split (",")
    
    calls = []
    for s in strings:
        parts = s.split ("|")
        if len (parts) > 3:
            name, notation, positions, every, from_ = parts
            calls.append (Call (name, notation, positions, every, from_))
        else:
            name, notation, positions = parts
            calls.append (Call (name, notation, positions))
    
    return calls


def calls_to_string (calls = []):
    return "[" + ",".join ([c.compact_string () for c in calls]) + "]"
