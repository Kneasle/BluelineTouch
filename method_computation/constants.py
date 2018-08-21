# BASIC CONSTANTS
bell_names = "1234567890ETABCDFGHIJKLMNOPQRSUVWXYZ"
touch_call_conversions = {"-": "B", "M": "P"}
touch_call_display_conversions = {"P": " ", "B": "-"}
all_stages = ["Zeros", "Ones", "Twos", "Singles", "Minimus", "Doubles", "Minor", "Triples", "Major", "Caters", "Royal",
			  "Cinques", "Maximus", "Sextuples", "Fourteen", "Septuples", "Sixteen", "Octuples", "Eighteen",
			  "Nonuples", "Twenty", "Decuples", "Twenty-two"]

calling_position_conversions = {"O": "B", "4": "F"}
place_notation_conversions = {"-": "X"}
name_escape_conversions = {
        "/": "@SL",
        "@": "@@",
        "\\": "@BS",
        "'": "@QT",
        "\"": "@DQ",
        "*": "@",
        ".": "@PD",
        "?": "@QM"
}

# ENUMS
ONLY_LEAD_HEADS = "Only Lead Ends"
ALL_TREBLE_LEADS = "All Treble Leads"
ALL_CHANGES = "All Changes"

ANY = "Any"

DESCENDING = "Descending"
ASCENDING = "Ascending"
BOTH = "Both"

CALL_SEQUENCE = "Call Sequence"
CALLING_POSITIONS = "Calling Positions"
BELLS_BEFORE = "Bells Before"

EVERY_LEAD = "Every Lead"
OVER_LEAD_HEAD = "Over Lead Head"

all_calling_types = [CALL_SEQUENCE, CALLING_POSITIONS, BELLS_BEFORE]

POSITIONS_BY_HEAVIEST_BELL = "Positions By Heaviest Bell"
POSITIONS_BY_PLACE = "Positions By Place"
POSITIONS_BY_PLACE_AFTER_CALL = "Positions By Place After Call"

END = "End"

TENOR = "Tenor"

STANDARD = "Standard"
ROUNDS = "Rounds"

HANDSTROKE = 0
BACKSTROKE = 1
