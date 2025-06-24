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
from wowsunpack.params import WoWsGameParams

class WoWsUnpack:

    def __init__(self, path):
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

    def _findLatestBinFolder(self):
        """
        Finds the latest folder in the bin folder
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

    def _validateFolder(self, path: str):
        """
        Make sure there are contains in path
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

    def _call(self, command: str):
        """
        Call wowsunpack.exe and make sure it was successful
        """
        # set shell to true for the pipe to work (writing to a file)
        p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        out, err = p.communicate()
        output = out.decode('utf-8')
        if 'ERROR' in output or p.returncode != 0:
            raise RuntimeError("wowsunpack.exe failed with output: " + output)

    def reset(self): 
        """
        Reset previous folders
        """
        self._resetDir('content')
        self._resetDir('gui')
        self._resetDir('spaces')
        self._resetDir('langs')
        self._resetDir('app/assets')
        print("done resetting\n")

    def writeContentList(self):
        """
        Writes the content list to a file, DEBUG ONLY
        """
        self._call(self._wowsunpack(list=True) + ' > contents.txt')
        print("done writing content list\n")

    def getListOf(self, filetype: str):
        """
        Get a list of files of a certain type
        """
        self._call(self._wowsunpack(list=True) + ' -I *.' + filetype + ' > hidden-' + filetype + '.txt')

    def search(self, query: str):
        """
        Search anything with the given query
        """
        self._call(self._wowsunpack(list=True) + ' -I ' + query + ' > search.txt')
        print("done searching\n")

    def unpackGameParams(self):
        """
        Unpacks *.data from the bin folder
        """
        self._call(self._wowsunpack() + ' -I content/*.data')
        print("done unpacking game params\n")

    def decodeGameParams(self):
        """
        Decodes GameParams.data from content folder
        """
        data_path = 'content/GameParams.data'
        if os.path.exists(data_path):
            gp = WoWsGameParams(data_path)
            print("decoding game params")
            gp.decode()
            print("done decoding game params\n")
        else:
            raise FileNotFoundError("GameParams.data not found")
    
    def unpack(self, query: str):
        """
        Unpack anything with the given query
        """
        self._call(self._wowsunpack() + ' -I ' + query)
        print("done unpacking {}\n".format(query))

    def unpackGameIcons(self):
        """
        Unpack game icons from the bin folder
        """
        self.unpack('gui/*.png -I gui/*.jpg')
        print("done unpacking game icons\n")

    def unpackGameGUI(self):
        """
        Unpack game GUI from the bin folder
        """
        self.unpack('gui/*')
        print("done unpacking game GUI\n")

    def unpackGameMaps(self):
        """
        Unpack game maps from the bin folder
        """
        self.unpack('spaces/*')
        print("done unpacking game icons\n")

    def decodeLanguages(self):
        """
        Decodes the language from global.mo
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

    def _resetDir(self, dirname: str):
        """
        Removes a directory if it exists and creates a new one.
        """
        if os.path.exists(dirname):
            shutil.rmtree(dirname)
        os.makedirs(dirname)

    def packAppAssets(self, output_path='./app/assets'):
        """
        Packs assets for WoWs Info
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
        for ship in os.listdir(gui_path + '/ship_previews'):
            if ship == 'placeholder.png' and not ship.endswith('.png'):
                continue

            shutil.copy(
                gui_path + '/ship_previews/' + ship,
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
