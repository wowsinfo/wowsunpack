from wowsunpack import WoWsUnpack

if __name__ == '__main__':
    unpack = WoWsUnpack('C:\Games\World_of_Warships')
    unpack.search('*prill*')
    unpack.unpackGameGUI()
