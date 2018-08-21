from .constants import *
from .change import *
import unicodedata


def convert_place_notation (notation):
    output = ""
    
    for i in notation:
        if i in place_notation_conversions.keys ():
            output += place_notation_conversions [i]
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
        if (places.__contains__ (bell_names [i]) or
                places.__contains__ (bell_names [i + 1])) or i >= stage - 1:
            transposition [i] = i
            i += 1
        else:
            transposition [i] = i + 1
            transposition [i + 1] = i
            i += 2
    
    return Change (stage, transposition)


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
    for i in name_escape_conversions.keys ():
        output = output.replace (i, name_escape_conversions [i])
    
    return output


def deescape_method_name (name):
    # CONVERT CHARACTERS
    for i in name_escape_conversions.keys ():
        name = name.replace (name_escape_conversions [i], i)
    
    # GENERATE UNICODE CHARACTERS
    while name.__contains__ ("*U"):
        index1 = name.index ("*U")
        index2 = name.index ("*V")
        name = name [:index1] + name [index1 + 2: index2] + name [index2 + 2:]
    
    return name


def convert_call_for_display (call_name):
    if call_name in touch_call_display_conversions.keys ():
        return touch_call_display_conversions [call_name]
    else:
        return call_name
