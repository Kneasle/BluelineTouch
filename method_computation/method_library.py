import os, io
from .constants import *
from .method import *
from .utilities import *


class MethodLibrary:
    def __init__ (self, path):
        self.path = path
        
        self.classifications = os.listdir (self.path)
        
        self.index = {}

        file = open (os.path.join (self.path, "index.txt"), mode = "r", encoding = "utf-8")
        
        for l in file:
            if l != "":
                key, value = l.split ("|")
                self.index [key] = value

        file.close ()
    
    def list_stages_in_classification (self, classification):
        return sorted (os.listdir (os.path.join (self.path, classification)), key = self.sorting_key)
    
    def list_methods (self, classification, stage):
        meths = os.listdir (os.path.join (self.path, classification, stage))
        for i in range (len (meths)):
            meths [i] = deescape_method_name (meths [i] [:-5])
        return sorted (meths)
    
    def get_method (self, classification = "Surprise", stage = "Major", title = "Bristol Surprise Major"):
        args = {}
        
        lines = open (os.path.join (self.path, classification, stage, title + ".meth"), "r", encoding = "utf-8").read ().splitlines ()
        
        for l in lines:
            ind = l.index ("|")
            key = l [:ind]
            value = l [ind + 1:]
            args [key] = value
        
        return Method (int (args ["stage"]), None, classification, args ["notation"], title = args ["title"])
    
    def get_method_by_title (self, title = "Bristol Surprise Major"):
        file_path = self.index [title]
        
        paths = file_path.replace ("\\", "/").split ("/")
        
        return self.get_method (paths [0], paths [1], paths [2].split (".") [0])
    
    def sorting_key (self, item):
        return all_stages.index (item)
