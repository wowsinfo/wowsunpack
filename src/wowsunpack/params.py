import struct
import zlib
import pickle
import json
import os
import sys
import shutil
from concurrent.futures import ThreadPoolExecutor
from types import ModuleType
from typing import Any, Dict, Tuple


# Add GameParams module to sys.modules
class GameParams(ModuleType):
    class TypeInfo(object): pass
    class GPData(object): pass
    # class GameParams: pass
    # class UIParams: pass
sys.modules[GameParams.__name__] = GameParams(GameParams.__name__)


class GPEncode(json.JSONEncoder):
    def default(self, o):
        try:
            for e in ['Cameras', 'DockCamera', 'damageDistribution', 'salvoParams']:
                o.__dict__.pop(e, o.__dict__)
            return o.__dict__
        except AttributeError:
            return {}


class WoWsGameParams:
    _subdir: str = 'split'

    def __init__(self, path: str):
        self.path = path

    def _mkdir(self, directory: str) -> None:
        """
        Create a directory if it doesn't exist.
        
        Args:
            directory: Path to the directory to create
        """
        if not os.path.exists(directory):
            os.makedirs(directory)

    def _writejson(self, _key: str, _value: Any, index: str) -> None:
        """
        Write a JSON file for a game parameter.
        
        Args:
            _key: The key name for the parameter
            _value: The value to write
            index: The index/subdirectory for organization
        """
        # Be resilient if typeinfo/type is missing
        try:
            t = _value.get('typeinfo', {}).get('type', 'UnknownType')
        except AttributeError:
            t = 'UnknownType'
        # If index is '', don't add a subdirectory for it
        if index:
            typedir = self._subdir + os.sep + str(index) + os.sep + str(t)
        else:
            typedir = self._subdir + os.sep + str(t)
        self._mkdir(typedir)

        with open(os.path.join(typedir, _key + '.json'), 'w', encoding='latin1') as ff:
            json.dump(_value, ff, sort_keys=True, indent=4, separators=(',', ': '))

    def _readRawData(self) -> Any:
        """
        Reads the raw data from the file and returns it as an object.
        
        Returns:
            Unpickled game parameters data
        """
        with open(self.path, 'rb') as f:
            gpd = f.read()
        gpd = struct.pack('B' * len(gpd), *gpd[::-1])
        gpd = zlib.decompress(gpd)
        gpd = pickle.loads(gpd, encoding='latin1')
        return gpd

    def dump_region(self, elem_dict: Any, region_key: str, filename: str) -> bool:
        """
        Dump a specific region from the game params to a file.
        
        Args:
            elem_dict: The dictionary containing game parameters
            region_key: The key of the region to dump
            filename: Output filename for the JSON file
            
        Returns:
            True if the region was found and dumped, False otherwise
        """
        if not isinstance(elem_dict, dict):
            return False
        if region_key in elem_dict:
            cleaned = json.loads(json.dumps({region_key: elem_dict[region_key]}, cls=GPEncode, ensure_ascii=False))
            with open(filename, 'w', encoding='latin1') as out:
                json.dump(cleaned, out, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': '))
            return True
        return False

    def decode(self) -> None:
        """
        Decodes the game params file and writes it to a JSON file.
        Creates GameParams-{index}.json with decoded game parameters.
        """
        gpd = self._readRawData()
        # Always unwrap the top-level '' key and write its contents directly
        if isinstance(gpd, (list, tuple)):
            for i, elem in enumerate(gpd):
                if isinstance(elem, dict) and '' in elem and isinstance(elem[''], dict):
                    cleaned = json.loads(json.dumps(elem[''], cls=GPEncode, ensure_ascii=False))
                    with open(f'GameParams-{i}.json', 'w', encoding='latin1') as out:
                        json.dump(cleaned, out, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': '))
                    break
        elif isinstance(gpd, dict) and '' in gpd and isinstance(gpd[''], dict):
            cleaned = json.loads(json.dumps(gpd[''], cls=GPEncode, ensure_ascii=False))
            with open('GameParams-0.json', 'w', encoding='latin1') as out:
                json.dump(cleaned, out, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': '))

    def split(self) -> None:
        """
        Decode the game params file and split it into multiple directories.
        Organizes parameters by type into separate JSON files.
        """
        gpd = self._readRawData()

        self._mkdir(self._subdir)

        # Locate the dictionary under key '' and split all its values
        # gpd may be a list/tuple of elements or a single dict
        source_dict = None
        if isinstance(gpd, (list, tuple)):
            for elem in gpd:
                if isinstance(elem, dict) and '' in elem and isinstance(elem[''], dict):
                    source_dict = elem['']
                    break
        elif isinstance(gpd, dict) and '' in gpd and isinstance(gpd[''], dict):
            source_dict = gpd['']

        if source_dict:
            # Clean via GPEncode then back to plain dict
            elemjson = json.loads(json.dumps(source_dict, cls=GPEncode, ensure_ascii=False))

            with ThreadPoolExecutor() as tpe:
                tpe.map(lambda p: self._writejson(*p), [(k, v, '') for k, v in elemjson.items()])


if __name__ == '__main__':
    gp = WoWsGameParams('GameParams.data')
    gp.decode()
    # gp.split()
