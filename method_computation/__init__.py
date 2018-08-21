from .method import *
from .change import *
from .touch import *
from .constants import *
from .classifications import *
from .method_library import *
from .example_methods import *
from .call import *
from .utilities import *

import os as __os

try:
        library = MethodLibrary (__os.path.join (os.path.split (__file__) [0], "Methods"))
except FileNotFoundError:
        library = None
