import method_computation.constants
import settings, utilities

# Generate table
if __name__ == "__main__":
    for i in range (4, 13):
        table_file = open ("Tables/" + method_computation.constants.all_stages [i] + ".txt", "w")
        table_file.write ("--" + method_computation.constants.all_stages [i] + "\n")
        for v in range (0, 2 ** i):
            binary = str (bin (v)) [2:]
            binary = "0" * (i - len (binary)) + binary
            if not binary.__contains__ ("101") and not binary.startswith ("01") and not binary.endswith ("10"):
                is_ligit = True
                splits = binary.split ("1") [:-1]
                for s in splits:
                    if len (s) % 2 == 1:
                        is_ligit = False
                        break

                if is_ligit:
                    place_notation = ""
                    for ind, b in enumerate (binary):
                        if b == "1":
                            place_notation += str (ind + 1)
                    if place_notation == "":
                        place_notation = "X"
                    table_file.write (place_notation + "|" + str (
                        utilities.split_notation_to_transposition (i, place_notation)) + "\n")

        table_file.close ()
