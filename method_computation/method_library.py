import os
import constants, method, utilities


class MethodLibrary:
    def __init__ (self, path):
        self.path = path
        
        self.classifications = os.listdir (self.path)
        
        self.index = {}
        
        lines = open (os.path.join (self.path, "index.txt"), "r").read ().decode ("utf8").splitlines ()
        for l in lines:
            if l != "":
                key, value = l.split ("|")
                self.index [key] = value
    
    def list_stages_in_classification (self, classification):
        return sorted (os.listdir (os.path.join (self.path, classification)), key = self.sorting_key)
    
    def list_methods (self, classification, stage):
        meths = os.listdir (os.path.join (self.path, classification, stage))
        for i in range (len (meths)):
            meths [i] = utilities.deescape_method_name (meths [i] [:-5])
        return sorted (meths)
    
    def get_method (self, classification = "Surprise", stage = "Major", title = "Bristol Surprise Major"):
        args = {}
        title = utilities.escape_method_name (title)
        
        lines = open (os.path.join (self.path, classification, stage, title + ".meth")).read ().splitlines ()
        
        for l in lines:
            key, value = l.split ("|")
            args [key] = value
        
        return method.Method (int (args ["stage"]), None, classification, args ["notation"], title = args ["title"])
    
    def get_method_by_title (self, title = "Bristol Surprise Major"):
        file_path = self.index [title]
        
        paths = file_path.split ("/")
        
        return self.get_method (paths [0], paths [1], paths [2].split (".") [0])
    
    def sorting_key (self, item):
        return constants.all_stages.index (item)
