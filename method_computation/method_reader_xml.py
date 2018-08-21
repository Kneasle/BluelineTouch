from bs4 import BeautifulSoup
import os
import utilities, constants, method, call

output_path = "/Users/christopherwhite-horne/Desktop/Methods"

print ("SOUPIFYING...")
soup = BeautifulSoup (open ("allmeths.xml", "r").read (), "html.parser")

print ("READING...")

files_done = 0

meths = soup.find_all ("method")

paths = {}

for p in meths:
    parent = p.parent
    properties = parent.find ("properties")
    classification = p.find ("classification")
    if classification is None:
        classification = properties.find ("classification")
    
    # region METHOD ARGS
    method_args = {}
    method_args ["title"] = p.find ("title").text
    method_args ["provisional"] = "false"
    method_args ["stage"] = str (properties.find ("stage").text)
    method_args ["url"] = "None"
    
    method_args ["classification"] = str (classification.text)
    if method_args ["classification"] == "":
        method_args ["classification"] = "Principle"
    
    method_args ["namemetaphone"] = "None"
    method_args ["notation"] = str (p.find ("notation").text)
    method_args ["notationexpanded"] = "None"
    
    try:
        method_args ["leadheadcode"] = str (p.find ("leadheadcode").text)
    except AttributeError:
        method_args ["leadheadcode"] = ""
    
    try:
        method_args ["leadhead"] = str (p.find ("leadHead").text)
    except AttributeError:
        pass
    method_args ["fchgroups"] = ""
    method_args ["numberofhunts"] = ""
    
    try:
        method_args ["little"] = classification ["little"]
    except KeyError:
        method_args ["little"] = "false"
    
    try:
        method_args ["differential"] = classification ["differential"]
    except KeyError:
        method_args ["differential"] = "false"
    
    try:
        method_args ["plain"] = classification ["plain"]
    except KeyError:
        method_args ["plain"] = "false"
    
    try:
        method_args ["trebledodging"] = classification ["trebledodging"]
    except KeyError:
        method_args ["trebledodging"] = "false"
    
    try:
        method_args ["lengthoflead"] = str (properties.find ("lengthoflead").text)
    except AttributeError:
        print (properties.prettify ())
    
    symmetry = str (properties.find ("symmetry").text)
    method_args ["palindromic"] = "false"
    method_args ["doublesym"] = "false"
    method_args ["rotational"] = "false"
    if "palindromic" in symmetry:
        method_args ["palindromic"] = "true"
    if "double" in symmetry:
        method_args ["doublesym"] = "true"
    if "rotational" in symmetry:
        method_args ["rotational"] = "true"
    # endregion
    
    # CREATE FILE STRUCTURE
    file_name = utilities.escape_method_name (method_args ["title"]) + ".meth"
    
    path_level_1 = output_path
    path_level_2 = os.path.join (path_level_1, method_args ["classification"])
    path_level_3 = os.path.join (path_level_2, constants.all_stages [int (method_args ["stage"])])
    path_level_4 = os.path.join (path_level_3, file_name)
    
    paths [method_args ["title"]] = os.path.join (
        method_args ["classification"], constants.all_stages [int (method_args ["stage"])], file_name
    )
    
    if not os.path.exists (path_level_1):
        os.mkdir (path_level_1)
    if not os.path.exists (path_level_2):
        os.mkdir (path_level_2)
    if not os.path.exists (path_level_3):
        os.mkdir (path_level_3)
    
    # GENERATE STANDARD CALLS
    try:
        meth = method.Method (
            stage = int (method_args ["stage"]),
            classification = method_args ["classification"],
            place_notation = method_args ["notation"],
            title = method_args ["title"]
        )
    except TypeError:
        print (method_args)
    
    method_args ["calls"] = call.calls_to_string (meth.calls)
    
    # WRITE FILE
    file = open (path_level_4, "w")
    for i in sorted (method_args.keys ()):
        file.write (i + "|" + method_args [i].encode ("utf8") + "\n")
    file.close ()
    
    # PRINT STATUS
    files_done += 1
    if files_done % 100 == 0:
        print (str (files_done) + " \t" + str (float (files_done) / float (len (meths)) * 100) + "%")

index_file = open (os.path.join (output_path, "index.txt"), "w")

for i in sorted (paths.keys ()):
    index_file.write ((i + "|" + paths [i] + "\n").encode ("utf8"))

index_file.close ()

print ("DONE")
