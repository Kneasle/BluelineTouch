from .constants import *
from .change import *

class Touch:
        def __init__ (self, methods, calls = "", method_calls = (0, [(0, 0)]), target_change = ROUNDS,
                calling_type = CALL_SEQUENCE, bell_calling_from = TENOR,
				  automatically_compute_changes = False, change_checks = ALL_CHANGES):
                self.methods = methods
                if not type (methods) is list:
                        self.methods = [methods]
                self.stage = max ([i.stage for i in self.methods])
                self.method_calls = method_calls
                self.calling_type = calling_type
                self.change_checks = change_checks
                self.bell_calling_from = bell_calling_from
                self.target_change = target_change

                # FIX ALTERNATE INPUTS
                if bell_calling_from == TENOR:
                        self.bell_calling_from = self.stage - 1
                if target_change is None:
                        self.target_change = rounds (self.stage)

                # GENERATE CALL ARRAY
                self.calls = []
                self.update_calls_from_string (calls)

        def update_calls_from_string (self, calls, call_type = None):
                if not call_type is None:
                        self.calling_type = call_type
                self.calls = []
                if self.calling_type == CALL_SEQUENCE:
                        for i in range (len (calls)):
                                call = calls [i].upper ()

                                # CONVERT CALLS THAT NEED TRANSLATING, e.g. "-" => "B", "P" => "M"
                                if call in touch_call_conversions:
                                        call = touch_call_conversions [call]

                                # DEAL WITH PLAIN LEADS
                                if call == "P":
                                        self.calls.append ("P")

                                # DEAL WITH ANY OTHER CALLS: if they are a ligit call, then include them, otherwise reject
                                has_found_ligit_call = False
                                for m in self.methods:
                                        if call in m.get_call_names ():
                                                has_found_ligit_call = True
                                                break

                                if has_found_ligit_call:
                                        self.calls.append (call)

                elif self.calling_type == CALLING_POSITIONS:
                        call_name = "B"
                        for i in range (len (calls)):
                                call = calls [i].upper ()

                                has_found_ligit_position = False
                                for m in self.methods:
                                        if call in m.get_call (call_name).calling_positions.values ():
                                                has_found_ligit_position = True

                                if not has_found_ligit_position:  # Try converting the calling positions
                                        converted_call = call
                                        if converted_call in calling_position_conversions.keys ():
                                                converted_call = calling_position_conversions [converted_call]

                                        for m in self.methods:
                                                if converted_call in m.calling_positions.values ():
                                                        has_found_ligit_position = True
                                                        call = converted_call

                                if has_found_ligit_position:
                                        self.calls.append (call_name + call)
                                        call_name = "B"

                                else:
                                        has_found_ligit_call_name = False
                                        corrected_call = call
                                        if corrected_call in touch_call_conversions.keys ():
                                                corrected_call = touch_call_conversions [corrected_call]

                                        for m in self.methods:
                                                if corrected_call in m.call_notations_dict.keys ():
                                                        has_found_ligit_call_name = True

                                        if has_found_ligit_call_name:
                                                call_name = corrected_call

                elif self.calling_type == BELLS_BEFORE:
                        call_name = "B"
                        lookup_string = str (rounds (self.stage))

                        for i in range (len (calls)):
                                call = calls [i].upper ()

                                if call in lookup_string:
                                        self.calls.append (call_name + call)
                                        call_name = "B"
                                else:
                                        corrected_call = call
                                        if corrected_call in touch_call_conversions.keys ():
                                                corrected_call = touch_call_conversions [corrected_call]

                                        for m in self.methods:
                                                if corrected_call in m.call_notations_dict.keys ():
                                                        call_name = corrected_call
