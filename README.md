# WoWsUnpack
[![License](https://img.shields.io/github/license/WoWs-Info/wows_unpack)](./LICENSE)

Based on [EdibleBug/WoWS-GameParams](https://github.com/EdibleBug/WoWS-GameParams), this fork uses `wowsunpack.exe` to extract `GameParams.data` before unpacking to `GameParams.json`.

[中文版本](./README-zh.md)

## Optional features
- Decode game languages
- Unpack game maps
- Unpack game icons
- Pack game assets

## Setup
- Use Python 3 and `python3 -m venv .env` to create a virtual environment
- Install dependencies with `pip install -r requirements.txt`
- Run `python3 run.py`
- Paste the game path into `game.path`
- Run `python3 run.py` again to unpack

## Use without Python
- Download the latest binary
- Double click on `run.exe`
- Paste the game path into `game.path`
- Double click on `run.exe` again to unpack

Windows may scan `run.exe` only for the first time. The binary is built with `pyinstaller`. `WoWsUnpack` is not responsible for anything if `pyinstaller` injects any malicious code while generating the binary. Please use the binary at your own risk.

## Arguments
- `--lang`: Decode game languages
- `--maps`: Unpack game maps
- `--icons`: Unpack all game icons
- `--assets`: Pack game assets into folders

Any other arguments are not valid. The program will exit with error code 1. Call the program like `./run.exe --lang` from the terminal. Double clicking will not pass in any arguments.

## Distribution
- Install `pyinstaller` following [this guide](https://pyinstaller.org/en/stable/index.html)
- Run `pyinstaller  --onefile .\run.py -p .\unpack\ --hidden-import GameParams`
- Copy `wowsunpack.exe` to `dist/`
- Ready to go!

***

# World of Warships GameParams to JSON
[![License](https://img.shields.io/github/license/EdibleBug/WoWS-GameParams)](https://github.com/EdibleBug/WoWS-GameParams/blob/master/LICENSE)

## Legal Notice and License
I acknowledge and agree to the rights and Terms of Use (ToS) provided by [Wargaming.net (WG)](https://wargaming.com/). Any users wishing to use the code or WoWSFT must also acknowledge and agree to the rights and ToS underlined by WG. I am not held responsible for any issues or problems that may occur related to using WoWSFT and/or provided codes.

Any codes and materials created by me are under [MIT License](https://github.com/EdibleBug/WoWS-GameParams/blob/master/LICENSE).

## Instruction
1. Use Python 3.
2. Legacy folder is outdated, do not use.
3. Extract GameParams.data into same folder.
    * OneFileToRuleThemAll.py
        * Extracts into a huge JSON file with everything included. This file is not intended for reading.
    * OneFileToSplitThemAll.py
        * Splits into many JSON files, with file name as key and value as content.
        * Example folder/file structure
          ```
          __ root
            |__ sub
               |__ 0
                  |__ Ability
                  |  |__ PCY001_CrashCrew.json
                  |  |__ ...
                  |__ Achievement
                  |  |__ PCH001_DoubleKill.json
                  |  |__ ...
                  |__ ...
          ```

Original codes from XeNTax forum, modified a while ago due to incompatibility with data.

[GameParams2Json](https://github.com/imkindaprogrammermyself/GameParams2Json) referenced when refactoring code.
