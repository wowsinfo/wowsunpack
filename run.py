import os
from src.unpack import WoWsUnpack

if __name__ == "__main__":
    print("Make sure the game path is valid!")
    print()
    print("Unpacking...")

    if os.path.exists('game.path'):
        with open('game.path', 'r') as f:
            path = f.read()
        unpack = WoWsUnpack(path)

        try:
            unpack.unpackGameParams()
            unpack.decodeGameParams()
            # optional actions
            # unpack.decodeLanguages()
            # unpack.unpackGameIcons()
            # unpack.unpackGameMaps()
        except FileNotFoundError:
            print("Make sure the game path is valid")
            print("\nhttps://github.com/WoWs-Info/wows_gameparams")
    else:
        with open('game.path', 'w') as f:
            print("Created game.path")
            print(
                "Please place your game path in it. It should look like C:\Games\World_of_Warships")
        exit(-1)
