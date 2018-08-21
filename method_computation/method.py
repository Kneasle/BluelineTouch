import change, utilities, constants, touch, call, classifications


class Method:
    def __init__ (self, stage = 8, name = None, classification = None, place_notation = "x18x18x18x18,12",
                  calls = constants.STANDARD, title = None, **kwargs):
        self.stage = stage
        self.name = name
        self.classification = classification
        self.title = title
        self.place_notation = place_notation
        self.calls = calls
        
        # region EXPAND NOTATIONS AND START LOOK-UP TABLE
        self.expanded_notation = utilities.full_notation_to_split_notation (self.place_notation)
        self.lookup_table = utilities.generate_look_up_table (self.expanded_notation, self.stage)
        # endregion
        
        # region GENERATE STATS
        self.lead_length = len (self.generate_plain_lead ())
        self.lead_head = self.generate_plain_lead () [-1]
        self.leads_in_plain_course = self.lead_head.order ()
        self.plain_course_length = self.lead_length * self.leads_in_plain_course
        self.half_lead_head = self.generate_plain_lead () [self.lead_length / 2 - 1]
        
        self.hunt_bells = []
        for i in range (self.stage):
            if self.lead_head [i] == i:
                self.hunt_bells.append (i)
        
        self.hunt_bell_paths = {}
        for i in self.hunt_bells:
            self.hunt_bell_paths [i] = []
            for c in self.generate_plain_lead ():
                self.hunt_bell_paths [i].append (c.index (i))
        # endregion
        
        # region FIX NAMES & TITLES
        if name is None:
            parts = title.split (" ")
            self.name = parts [0]
            
            if len (parts) > 2:
                self.classification = parts [1]
            else:
                if self.hunt_bells == []:
                    # NO HUNT BELLS ==> PRINCIPLE
                    self.classification = classifications.PRINCIPLE
                else:
                    self.classification = classifications.BOB
        
        if title is None:
            if self.classification is classifications.PRINCIPLE:
                self.title = self.name + " " + constants.all_stages [self.stage]
            else:
                self.title = self.name + " " + self.classification + " " + constants.all_stages [self.stage]
        # endregion
        
        # region COMPUTE CALL DATA
        if self.calls == constants.STANDARD:
            self.calls = utilities.generate_standard_bobs_and_singles (self)
        elif type (self.calls) is str:
            self.calls = call.calls_from_string (self.calls)
        elif type (self.calls) is dict:
            self.calls = [call.Call (i, self.calls [i]) for i in self.calls.keys ()]
        
        for c in self.calls:
            c.set_method (self)
        # endregion
    
    def generate_plain_lead (self):
        changes = []
        current_change = change.rounds (self.stage)
        for n in self.expanded_notation:
            current_change = current_change.transpose (self.lookup_table [n])
            changes.append (current_change)
        return changes
    
    def generate_plain_course (self):
        return touch.Touch (self)
    
    def dump_stats (self):
        return utilities.create_dump ({
            "Title": self.title,
            "Place Notation": self.place_notation,
            "Expanded Notation": self.expanded_notation,
            "Lead Length": self.lead_length,
            "Lead Head": self.lead_head,
            "Calls": self.calls,
            "Hunt Bells": self.hunt_bells,
            "Hunt Bell Paths": self.hunt_bell_paths,
            "Plain Course Length": self.plain_course_length,
            "Half Lead Head": self.half_lead_head
        })
    
    def get_call (self, name):
        for i in self.calls:
            if i.name == name:
                return i
        return None
    
    def get_call_names (self):
        return [c.name for c in self.calls]
    
    def __str__ (self):
        return self.title + ": " + self.place_notation + " {" + ", ".join ([str (c) for c in self.calls]) + "}"
