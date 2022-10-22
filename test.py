from wowsunpack import WoWsUnpack

if __name__ == '__main__':
    unpack = WoWsUnpack('C:\Games\World_of_Warships')
    unpack.search('*prill*')

import sys
sys.argv = ['', '--lang', '--icons', '--maps', '--assets']
import wowsunpack.__main__