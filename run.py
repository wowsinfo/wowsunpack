import os
import sys
from unpack import WoWsUnpack
import traceback

if __name__ == "__main__":
    print("Make sure the game path is valid!")
    print()
    print("Unpacking...")

    def exit_program(code: int):
        input("Press enter to exit...")
        sys.exit(code)


    if os.path.exists('game.path'):
        with open('game.path', 'r') as f:
            path = f.read().strip()
        unpack = WoWsUnpack(path)

        try:
            unpack.unpackGameParams()
            unpack.decodeGameParams()

            # optional actions
            # unpack.decodeLanguages()
            # unpack.unpackGameIcons()
            # unpack.unpackGameMaps()
        except FileNotFoundError:
            print("Make sure the game path is valid. It should look like C:\Games\World_of_Warships")
            print("\nhttps://github.com/WoWs-Info/wows_gameparams")
            exit_program(-1)
        except:
            traceback.print_exc()
            exit_program(-1)
    else:
        with open('game.path', 'w') as f:
            print("Created game.path")
            print(
                "Please place your game path in it. It should look like C:\Games\World_of_Warships")
            print("\nhttps://github.com/WoWs-Info/wows_gameparams")
            exit_program(-1)

    print("Done unpacking!")
    exit_program(0)
