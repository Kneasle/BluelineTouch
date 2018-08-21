import os
import constants, utilities


output_path = "Methods2"

text = open ("../meths.txt", "r").read ().split ("\n")

headers = text [0].split (",")

if not os.path.exists (output_path):
	os.mkdir (output_path)

for i in text [1:]:
	# DECODE LINE
	string = ""
	in_quotes = False
	line = []
	for p in i:
		if p == "," and not in_quotes:
			line.append (string)
			string = ""
		elif p == "\"":
			in_quotes = not in_quotes
		else:
			string += p
	line.append (string)

	# CREATE FILE/PATH
	stage = constants.all_stages [int (line [headers.index ("stage")])]
	classification = line [headers.index ("classification")]
	name = line [headers.index ("title")]

	if classification == "":
		if "Differential" in name:
			classification = line [headers.index ("classification")] = "Differential"
		else:
			classification = line [headers.index ("classification")] = "Principle"

	if not os.path.exists (os.path.join (output_path, classification)):
		os.mkdir (os.path.join (output_path, classification))

	if not os.path.exists (os.path.join (output_path, classification, stage)):
		os.mkdir (os.path.join (output_path, classification, stage))

	path = os.path.join (output_path, classification, stage, utilities.escape_method_name (name) + ".meth")
	if not os.path.exists (path):
		meth_file = open (path, "w")

		for i in range (len (headers)):
			try:
				meth_file.write (headers [i] + "|" + line [i] + "\n")
			except IndexError:
				meth_file.write (headers [i] + "|\n")

		meth_file.close ()

print (headers)
