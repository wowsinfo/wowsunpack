import sys
import os
# this is necessary for submodules to work correctly
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from unpack.unpack import WoWsUnpack
from unpack.WoWsGameParams import WoWsGameParams
