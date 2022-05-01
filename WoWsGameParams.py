import struct
import zlib
import pickle
import json
import os
import sys
import shutil
from concurrent.futures import ThreadPoolExecutor
sys.path.append('wows_gameparams')


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

    def _mkdir(self, directory: str):
        if not os.path.exists(directory):
            os.makedirs(directory)

    def _writejson(self, _key, _value, index):
        # note: _subdir is a global
        typedir = self._subdir + os.sep + \
            str(index) + os.sep + _value['typeinfo']['type']
        self._mkdir(typedir)

        with open(os.path.join(typedir, _key + '.json'), 'w', encoding='latin1') as ff:
            json.dump(_value, ff, sort_keys=True,
                      indent=4, separators=(',', ': '))

    def _readRawData(self):
        '''
        Reads the raw data from the file and returns it as an object
        '''
        with open(self.path, 'rb') as f:
            gpd = f.read()
        gpd = struct.pack('B' * len(gpd), *gpd[::-1])
        gpd = zlib.decompress(gpd)
        gpd = pickle.loads(gpd, encoding='latin1')
        return gpd

    def decode(self):
        '''
        Decodes the game params file and writes it to a json file
        '''
        gpd = self._readRawData()

        for index, elem in enumerate(gpd):
            if not isinstance(elem, dict):
                continue

            with open('GameParams-' + str(index) + '.json', 'w', encoding='latin1') as ff:
                json.dump(elem, ff, cls=GPEncode, sort_keys=True,
                          indent=4, separators=(',', ': '))

    def split(self):
        '''
        Decode the game params file and split it into multiple directories
        '''
        gpd = self._readRawData()

        self._mkdir(self._subdir)

        for index, elem in enumerate(gpd):
            if not isinstance(elem, dict):
                continue

            elemjson = json.dumps(elem, cls=GPEncode, ensure_ascii=False)
            elemjson = json.loads(elemjson)

            with ThreadPoolExecutor() as tpe:
                tpe.map(lambda p: self._writejson(*p),
                        [(k, v, index) for k, v in elemjson.items()])


if __name__ == '__main__':
    gp = WoWsGameParams('GameParams.data')
    gp.decode()
    gp.split()
