import os
import sys
from unpack import WoWsUnpack
import traceback

def exit_program(code: int):
    input("Press enter to exit...")
    sys.exit(code)

if __name__ == "__main__":
    print("Make sure the game path is valid!")
    print()
    print("Unpacking...")

    decodeLang = False
    unpackIcons = False
    unpackMaps = False
    packAssets = False

    arguments = sys.argv[1:]
    if len(arguments) > 0:
        for arg in arguments:
            if arg == "--lang":
                decodeLang = True
            elif arg == "--icons":
                unpackIcons = True
            elif arg == "--maps":
                unpackMaps = True
            elif arg == "--assets":
                packAssets = True
            else:
                print("Unknown argument: " + arg)
                exit_program(-1)

    if os.path.exists('game.path'):
        with open('game.path', 'r') as f:
            path = f.read().strip()
        unpack = WoWsUnpack(path)
        # unpack.unpackGameGUI()
        unpack.getListOf('swf')
        exit(0)

        try:
            unpack.unpackGameParams()
            unpack.decodeGameParams()

            # optional actions
            if unpackIcons:
                print("Unpacking icons...")
                unpack.unpackGameIcons()
            if unpackMaps:
                print("Unpacking maps...")
                unpack.unpackGameMaps()
            if decodeLang:
                print("Decoding language files...")
                unpack.decodeLanguages()
            if packAssets:
                print("Packing assets...")
                unpack.packAppAssets(output_path='assets/')
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
