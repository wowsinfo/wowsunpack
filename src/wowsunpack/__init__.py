"""
Unpack World of Warships game files.
"""

__version__ = '0.0.1'
__all__ = ['WoWsUnpack']


import json
import gnu_mo_files as mo
import shutil
import pathlib
import os
import sys
import subprocess
from pathlib import Path
from typing import Optional, List
from wowsunpack.params import WoWsGameParams

class WoWsUnpack:

    def __init__(self, path: str):
        """
        Initialize WoWsUnpack with the game installation path.
        
        Args:
            path: The root path of World of Warships installation
            
        Raises:
            FileNotFoundError: If wowsunpack.exe is not found
        """
        self.path = path

        # wowsunpack is under the same folder
        self._unpack_path = os.path.dirname((__file__)) + '/wowsunpack.exe'
        print("wowsunpack path: " + self._unpack_path)
        # fix the path issue for exe mode
        if getattr(sys, 'frozen', False):
            self._unpack_path = str(Path(sys._MEIPASS)) + '/wowsunpack.exe'
            # print("unpack path: " + self._unpack_path)

        # make sure wowsunpack.exe if available
        if not os.path.exists(self._unpack_path):
            raise FileNotFoundError("wowsunpack.exe not found")

    def _findLatestBinFolder(self) -> str:
        """
        Finds the latest folder in the bin folder.
        
        Returns:
            The name of the latest bin folder (as a string number)
            
        Raises:
            FileNotFoundError: If no bin folders are found
        """
        bin_path = "{}/bin".format(self.path)
        bin_folders = os.listdir(bin_path)
        if (len(bin_folders) == 0):
            raise FileNotFoundError("No bin folders found in: " + bin_path)
        # remove all files in bin folder and make sure folders are all numbers
        bin_folders = [f for f in bin_folders if os.path.isdir(bin_path + '/' + f) and f.isdigit()]
        # ensure to compare as integers but by string
        bin_folders.sort(key=int)

        return bin_folders[-1]

    def _validateFolder(self, path: str) -> None:
        """
        Make sure there are contents in path.
        
        Args:
            path: The directory path to validate
            
        Raises:
            FileNotFoundError: If the folder doesn't exist or is empty
        """
        if not os.path.exists(path):
            raise FileNotFoundError("Folder not found: " + path)
        if len(os.listdir(path)) == 0:
            raise FileNotFoundError("Folder is empty: " + path)

    def _wowsunpack(self, list: bool = False) -> str:
        latest_bin = self._findLatestBinFolder()
        print("Latest bin folder: " + latest_bin)
        flag = '-l' if list else '-x'
        return '{} {} "{}/bin/{}/idx" -p ../../../res_packages'.format(self._unpack_path, flag, self.path, latest_bin)

    def _call(self, command: str) -> None:
        """
        Call wowsunpack.exe and make sure it was successful.
        
        Args:
            command: The command string to execute
            
        Raises:
            RuntimeError: If wowsunpack.exe fails or returns an error
        """
        # set shell to true for the pipe to work (writing to a file)
        p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        out, err = p.communicate()
        output = out.decode('utf-8')
        if 'ERROR' in output or p.returncode != 0:
            raise RuntimeError("wowsunpack.exe failed with output: " + output)

    def reset(self) -> None: 
        """
        Reset previous folders by removing and recreating them.
        This clears content, gui, spaces, langs, and app/assets directories.
        """
        self._resetDir('content')
        self._resetDir('gui')
        self._resetDir('spaces')
        self._resetDir('langs')
        self._resetDir('app/assets')
        print("done resetting\n")

    def writeContentList(self) -> None:
        """
        Writes the content list to a file. DEBUG ONLY.
        Creates a contents.txt file with all available files in the game archive.
        """
        self._call(self._wowsunpack(list=True) + ' > contents.txt')
        print("done writing content list\n")

    def getListOf(self, filetype: str) -> None:
        """
        Get a list of files of a certain type.
        
        Args:
            filetype: The file extension to search for (e.g., 'png', 'data')
        """
        self._call(self._wowsunpack(list=True) + ' -I *.' + filetype + ' > hidden-' + filetype + '.txt')

    def search(self, query: str) -> None:
        """
        Search anything with the given query and save results to search.txt.
        
        Args:
            query: Search pattern (supports wildcards like *.png or folder/*)
        """
        self._call(self._wowsunpack(list=True) + ' -I ' + query + ' > search.txt')
        print("done searching\n")

    def unpackGameParams(self) -> None:
        """
        Unpacks *.data files from the bin folder (mainly GameParams.data).
        """
        self._call(self._wowsunpack() + ' -I content/*.data')
        print("done unpacking game params\n")

    def decodeGameParams(self) -> None:
        """
        Decodes GameParams.data from content folder to JSON format.
        
        Raises:
            FileNotFoundError: If GameParams.data is not found in content folder
        """
        data_path = 'content/GameParams.data'
        if os.path.exists(data_path):
            gp = WoWsGameParams(data_path)
            print("decoding game params")
            gp.decode()
            print("done decoding game params\n")
        else:
            raise FileNotFoundError("GameParams.data not found")
    
    def unpack(self, query: str) -> None:
        """
        Unpack files matching the given query pattern.
        This is a generic unpacking method that can extract any files from the game archive.
        
        Args:
            query: Pattern to match files (supports wildcards)
                   Examples:
                   - 'gui/*.png' - All PNG files in gui folder
                   - 'content/*.data' - All data files in content folder
                   - 'spaces/*' - Everything in spaces folder
                   - 'gui/*.png -I gui/*.jpg' - Multiple patterns
        
        Example:
            >>> unpacker = WoWsUnpack('C:/Games/World_of_Warships')
            >>> unpacker.unpack('gui/achievements/*.png')  # Unpack only achievement icons
            >>> unpacker.unpack('content/GameParams.data')  # Unpack specific file
        """
        self._call(self._wowsunpack() + ' -I ' + query)
        print("done unpacking {}\n".format(query))

    def unpack_folder(self, folder_path: str, file_pattern: str = '*', exclude_patterns: Optional[List[str]] = None) -> None:
        """
        Unpack a specific folder or selective files from the game archive.
        This is a high-level method for selective unpacking to improve performance.
        
        Args:
            folder_path: The folder path to unpack (e.g., 'gui', 'content', 'spaces', 'gui/achievements')
            file_pattern: File pattern to match within the folder (default: '*' for all files)
                         Examples: '*.png', '*.data', 'icon_*', etc.
            exclude_patterns: Optional list of patterns to exclude
        
        Example:
            >>> unpacker = WoWsUnpack('C:/Games/World_of_Warships')
            >>> # Unpack only achievement icons
            >>> unpacker.unpack_folder('gui/achievements', '*.png')
            >>> 
            >>> # Unpack all GUI files
            >>> unpacker.unpack_folder('gui')
            >>> 
            >>> # Unpack only game params
            >>> unpacker.unpack_folder('content', '*.data')
            >>> 
            >>> # Unpack PNG files but exclude specific ones
            >>> unpacker.unpack_folder('gui/consumables', '*.png', exclude_patterns=['*_empty.png'])
        """
        # Normalize folder path (remove leading/trailing slashes)
        folder_path = folder_path.strip('/')
        
        # Build the query pattern
        query = f"{folder_path}/{file_pattern}"
        
        # Add exclude patterns if provided
        if exclude_patterns:
            for exclude in exclude_patterns:
                query += f" -E {folder_path}/{exclude}"
        
        print(f"Unpacking from folder: {folder_path} with pattern: {file_pattern}")
        self._call(self._wowsunpack() + ' -I ' + query)
        print(f"done unpacking from {folder_path}\n")

    def unpackGameIcons(self) -> None:
        """
        Unpack game icons (PNG and JPG files) from the gui folder.
        """
        self.unpack('gui/*.png -I gui/*.jpg')
        print("done unpacking game icons\n")

    def unpackGameGUI(self) -> None:
        """
        Unpack all game GUI files from the gui folder.
        """
        self.unpack('gui/*')
        print("done unpacking game GUI\n")

    def unpackGameMaps(self) -> None:
        """
        Unpack game maps from the spaces folder.
        """
        self.unpack('spaces/*')
        print("done unpacking game maps\n")

    def decodeLanguages(self) -> None:
        """
        Decodes language files from global.mo to JSON format.
        Processes all available language folders and outputs them to langs/ directory.
        """
        latest_bin = self._findLatestBinFolder()
        language_folder = '{}\\bin\\{}\\res\\texts'.format(
            self.path, latest_bin)

        self._resetDir('langs')
        # only decode en, zh and jp
        for folder in os.listdir(language_folder):
            # if folder in ['en', 'zh', 'ja']:
            decoded_dict = mo.read_mo_file(
                language_folder + '\\' + folder + '\\LC_MESSAGES\\global.mo')
            del decoded_dict['']
            with open('langs/{}_lang.json'.format(folder), 'w', encoding="utf-8") as outfile:
                json_str = json.dumps(decoded_dict, ensure_ascii=False)
                outfile.write(json_str)

        print("done decoding languages\n")

    def _resetDir(self, dirname: str) -> None:
        """
        Removes a directory if it exists and creates a new one.
        
        Args:
            dirname: Name of the directory to reset
        """
        if os.path.exists(dirname):
            shutil.rmtree(dirname)
        os.makedirs(dirname)

    def packAppAssets(self, output_path: str = './app/assets') -> None:
        """
        Packs assets for WoWs Info application.
        Extracts and organizes game assets into categorized folders.
        
        Args:
            output_path: Output directory for packed assets (default: './app/assets')
            
        Raises:
            FileNotFoundError: If gui folder is not found or required folders are empty
        """
        gui_path = 'gui'
        # TODO: to be updated when finalised
        self._resetDir(output_path)
        if not os.path.exists(gui_path):
            raise FileNotFoundError("gui folder not found")

        # TODO: code duplication, should be refactored
        # ACHIEVEMENTS
        self._resetDir(output_path + '/achievements')
        for achievement in os.listdir(gui_path + '/achievements'):
            # remove grey icons and two placeholders
            if achievement in ['icon_achievement.png', 'placeholder.png']:
                continue
            if '_des.png' in achievement:
                continue

            formatted_name = achievement.replace(
                'icon_achievement_', ''
            )
            shutil.copy(
                gui_path + '/achievements/' + achievement,
                output_path + '/achievements/' + formatted_name,
            )
        self._validateFolder(output_path + '/achievements')

        # SHIPS
        self._resetDir(output_path + '/ships')
        ship_previews_path = gui_path + '/ship_previews'
        for ship in os.listdir(ship_previews_path):
            ship_path = os.path.join(ship_previews_path, ship)
            # Skip if not a file (e.g., skip directories like 'medium')
            if not os.path.isfile(ship_path):
                continue
            if ship == 'placeholder.png' and not ship.endswith('.png'):
                continue

            shutil.copy(
                ship_path,
                output_path + '/ships/' + ship,
            )
        self._validateFolder(output_path + '/ships')

        # UPGRADES
        self._resetDir(output_path + '/upgrades')
        for modernization in os.listdir(gui_path + '/modernization_icons'):
            formatted_name = modernization.replace(
                'icon_modernization_', ''
            )
            shutil.copy(
                gui_path + '/modernization_icons/' + modernization,
                output_path + '/upgrades/' + formatted_name,
            )
        self._validateFolder(output_path + '/upgrades')

        # FLAGS
        self._resetDir(output_path + '/flags')
        for flag in os.listdir(gui_path + '/signal_flags'):
            if '_des.png' in flag:
                continue
            shutil.copy(
                gui_path + '/signal_flags/' + flag,
                output_path + '/flags/' + flag,
            )
        self._validateFolder(output_path + '/flags')

        # CAMOUFLAGES
        self._resetDir(output_path + '/camouflages')
        for camouflage in os.listdir(gui_path + '/exteriors/camouflages'):
            if not camouflage.startswith('PCEC'):
                continue
            if '_des.png' in camouflage:
                continue
            shutil.copy(
                gui_path + '/exteriors/camouflages/' + camouflage,
                output_path + '/camouflages/' + camouflage,
            )
        self._validateFolder(output_path + '/camouflages')

        # PERMOFLAGES
        self._resetDir(output_path + '/permoflages')
        for permoflage in os.listdir(gui_path + '/exteriors/permoflages'):
            if '_des.png' in permoflage:
                continue
            shutil.copy(
                gui_path + '/exteriors/permoflages/' + permoflage,
                output_path + '/permoflages/' + permoflage,
            )
        self._validateFolder(output_path + '/permoflages')

        # COMMANDER SKILLS
        self._resetDir(output_path + '/skills')
        for skill in os.listdir(gui_path + '/crew_commander/skills'):
            formatted_name = ''.join([x.title() for x in skill.split('_')])
            # make sure the format is not Png but png, this is causing some issues on web
            formatted_name = formatted_name.replace('.Png', '.png')
            shutil.copy(
                gui_path + '/crew_commander/skills/' + skill,
                output_path + '/skills/' + formatted_name,
            )
        self._validateFolder(output_path + '/skills')

        # CONSUMABLES
        self._resetDir(output_path + '/consumables')
        for consumable in os.listdir(gui_path + '/consumables'):
            if not consumable.startswith('consumable_'):
                continue

            if '_empty.png' in consumable or 'undefined.png' in consumable:
                continue

            formatted_name = consumable.replace('consumable_', '')
            shutil.copy(
                gui_path + '/consumables/' + consumable,
                output_path + '/consumables/' + formatted_name,
            )
        self._validateFolder(output_path + '/consumables')

        # count the overall size of assets
        root_directory = pathlib.Path(output_path)
        assets_size = sum(
            f.stat().st_size for f in root_directory.glob('**/*') if f.is_file()
        ) / 1024 / 1024
        print("done packing assets, size: {:.2f} MB".format(assets_size))
