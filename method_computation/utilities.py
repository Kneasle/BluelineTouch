import constants, change, call
import unicodedata


def convert_place_notation (notation):
    output = ""
    
    for i in notation:
        if i in constants.place_notation_conversions.keys ():
            output += constants.place_notation_conversions [i]
        else:
            output += i
    
    return output


def full_notation_to_split_notation (notation):
    notation = convert_place_notation (notation)
    
    notations = []
    notation_so_far = ""
    comma_state = "None"
    for i in notation:
        if i == ".":
            notations.append (notation_so_far)
            notation_so_far = ""
        elif i == ",":
            notations.append (notation_so_far)
            notation_so_far = ""
            if len (notations) <= 1:
                comma_state = "Start"
            else:
                comma_state = "End"
        elif i.upper () == "X":
            if notation_so_far != "":
                notations.append (notation_so_far)
            notations.append ("X")
            notation_so_far = ""
        else:
            notation_so_far += i
    
    if notation_so_far != "":
        notations.append (notation_so_far)
    
    if comma_state == "None":
        return notations
    elif comma_state == "End":
        central_notation = notations [:-2]
        reversed_central = central_notation [:]
        reversed_central.reverse ()
        half_lead = notations [-2]
        lead_head = notations [-1]
        return central_notation + [half_lead] + reversed_central + [lead_head]
    elif comma_state == "Start":
        central_notation = notations [1:-1]
        reversed_central = central_notation [:]
        reversed_central.reverse ()
        half_lead = notations [0]
        lead_head = notations [-1]
        return [half_lead] + central_notation + [lead_head] + reversed_central


def split_notation_to_transposition (stage, notation):
    places = []
    if notation == "X":
        places = []
    else:
        for i in range (len (notation)):
            places.append (notation [i])
    
    transposition = [p for p in range (stage)]
    i = 0
    while i < stage:
        if (places.__contains__ (constants.bell_names [i]) or
                places.__contains__ (constants.bell_names [i + 1])) or i >= stage - 1:
            transposition [i] = i
            i += 1
        else:
            transposition [i] = i + 1
            transposition [i + 1] = i
            i += 2
    
    return change.Change (stage, transposition)


def generate_look_up_table (expanded_notation, stage):
    notations_used = list (set (expanded_notation))
    lookup_table = {}
    for i in notations_used:
        lookup_table [i] = split_notation_to_transposition (stage, i).sequence
    return lookup_table


def create_dump (dictionary):
    string = ""
    for i in sorted (dictionary.keys ()):
        string += str (i) + ": " + str (dictionary [i]) + "\n"
    return string [:-1]


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
                    return [call.Call ("B", "14", "IBF" + call_set), call.Call ("S", "1234", "23F" + call_set)]
                else:
                    return [call.Call ("B", "14"), call.Call ("S", "1234")]
            elif method.stage == 5:
                #  -- B: 145, S: 123
                return [call.Call ("B", "145", "IBMH"), call.Call ("S", "123", "23WH")]
        
        # CASE 2: "18" LEAD HEAD
        if method.expanded_notation [-1] == "1" + constants.bell_names [method.stage - 1] and \
                                method.stage % 2 == 0 and call_set is not None:
            pivot_bell = method.half_lead_head [
                constants.bell_names.index (method.expanded_notation [method.lead_length / 2 - 1] [0])
            ]
            
            if pivot_bell == 1:
                # BRISTOL/KENT-LIKE "18" LEAD END, WITH 2 AS PIVOT BELL -- B: 14, S: 1234
                return [call.Call ("B", "14", "IBF" + call_set), call.Call ("S", "1234", "23F" + call_set)]
            else:
                # TODO: FIX CALLING POSITION NAMES FOR Nth PLACE METHODS
                # PRIMROSE-LIKE "18" LEAD END, WITHOUT 2 AS PIVOT BELL -- B: 1{n-2}, S: 1{n-2}{n-1}{n}
                return [
                    call.Call ("B", "1" + constants.bell_names [method.stage - 3], "IBF" + call_set),
                    call.Call ("S", "1" + constants.bell_names [method.stage - 3: method.stage], "23F" + call_set)
                ]
    
    return []


def get_unrepeated_string (string):
    # LOOK FOR REPEATS
    for i in range (1, len (string)):
        if len (string) % i == 0:
            comparitor_string = string [:i]
            has_found_flaw = False
            for j in range (1, len (string) / i):
                if string [j * i: (j + 1) * i] != comparitor_string:
                    has_found_flaw = True
                    break
            if not has_found_flaw:
                return comparitor_string
    
    return string


def get_unrepeated_array (array):
    # LOOK FOR REPEATS
    for i in range (1, len (array)):
        if len (array) % i == 0:
            comparitor_array = array [:i]
            has_found_flaw = False
            for j in range (1, len (array) / i):
                if array [j * i: (j + 1) * i] != comparitor_array:
                    has_found_flaw = True
                    break
            if not has_found_flaw:
                return comparitor_array
    
    return array


def escape_method_name (name):
    output = ""
    
    # ESCAPE UNICODE CHARACTERS
    for i in list (name):
        try:
            output += str (i)
        except UnicodeEncodeError:
            output += "*U" + str (unicodedata.normalize ('NFKD', i).encode ('ascii', 'backslashreplace')) [3:] + "*V"
    
    # CONVERT CHARACTERS
    for i in constants.name_escape_conversions.keys ():
        output = output.replace (i, constants.name_escape_conversions [i])
    
    return output


def deescape_method_name (name):
    # CONVERT CHARACTERS
    for i in constants.name_escape_conversions.keys ():
        name = name.replace (constants.name_escape_conversions [i], i)
    
    # GENERATE UNICODE CHARACTERS
    while name.__contains__ ("*U"):
        index1 = name.index ("*U")
        index2 = name.index ("*V")
        name = name [:index1] + name [index1 + 2: index2] + name [index2 + 2:]
    
    return name


def convert_call_for_display (call_name):
    if call_name in constants.touch_call_display_conversions.keys ():
        return constants.touch_call_display_conversions [call_name]
    else:
        return call_name
