from .utilities import *
from .constants import *


class Call:
    def __init__ (self, name, place_notation, calling_positions = None, every = EVERY_LEAD,
                  _from = OVER_LEAD_HEAD):
        self.name = name
        self.place_notation = place_notation
        self.expanded_notation = full_notation_to_split_notation (self.place_notation)
        self.every = every
        self.from_ = _from
        self.calling_positions = calling_positions
        if self.from_ == OVER_LEAD_HEAD:
            self.from_ = - (len (self.expanded_notation) - 1)
        
        self.lookup_table = None
        self.method = None
    
    def set_method (self, method):
        self.method = method
        
        if self.every == EVERY_LEAD:
            self.every = method.lead_length
        
        self.lookup_table = generate_look_up_table (self.expanded_notation, self.method.stage)
    
    def __str__ (self):
        return self.name + ": " + str (self.place_notation) + " (every: " + str (self.every) + ", from: " + \
               str (self.from_) + ", calling positions: " + str (self.calling_positions) + ")"
    
    def __len__ (self):
        return len (self.expanded_notation)
    
    def __repr__ (self):
        return self.__str__ ()
    
    def compact_string (self):
        if self.every == EVERY_LEAD:
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


def generate_standard_bobs_and_singles (method):
    if method.hunt_bells == [0]:
        try:
            call_set = {
                6: "WH",
                7: "WMH",
                8: "VMWH",
                9: "VXWMH",
                10: "VXSMWH",
                11: "VXSEWMH",
                12: "VXSENMWH",
                13: "VXSEN?WMH",
            } [method.stage]
        except KeyError:
            call_set = None
        
        # CASE 1: PLAIN BOB-LIKE "12" LEAD HEAD
        if "12" in method.expanded_notation [-1]:
            if method.stage >= 6:
                #  -- B: 14, S: 1234
                if not call_set is None:
                    return [Call ("B", "14", "IBF" + call_set), Call ("S", "1234", "23F" + call_set)]
                else:
                    return [Call ("B", "14"), Call ("S", "1234")]
            elif method.stage == 5:
                #  -- B: 145, S: 123
                return [Call ("B", "145", "IBMH"), Call ("S", "123", "23WH")]
        
        # CASE 2: "18" LEAD HEAD
        if method.expanded_notation [-1] == "1" + bell_names [method.stage - 1] and \
                                method.stage % 2 == 0 and call_set is not None:
            pivot_bell = method.half_lead_head [
                bell_names.index (method.expanded_notation [method.lead_length // 2 - 1] [0])
            ]
            
            if pivot_bell == 1:
                # BRISTOL/KENT-LIKE "18" LEAD END, WITH 2 AS PIVOT BELL -- B: 14, S: 1234
                return [Call ("B", "14", "IBF" + call_set), Call ("S", "1234", "23F" + call_set)]
            else:
                # TODO: FIX CALLING POSITION NAMES FOR Nth PLACE METHODS
                # PRIMROSE-LIKE "18" LEAD END, WITHOUT 2 AS PIVOT BELL -- B: 1{n-2}, S: 1{n-2}{n-1}{n}
                return [
                    Call ("B", "1" + bell_names [method.stage - 3], "IBF" + call_set),
                    Call ("S", "1" + bell_names [method.stage - 3: method.stage], "23F" + call_set)
                ]
    
    return []
