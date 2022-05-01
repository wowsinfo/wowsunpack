import struct
import zlib
import pickle
import json
import os
import shutil
from concurrent.futures import ThreadPoolExecutor


class GPEncode(json.JSONEncoder):
    def default(self, o):
        try:
            for e in ['Cameras', 'DockCamera', 'damageDistribution', 'salvoParams']:
                o.__dict__.pop(e, o.__dict__)
            return o.__dict__
        except AttributeError:
            return {}


class WoWsGameParams:
    def __init__(self, path: str):
        self.path = path

    def _mkdir(self, subdir):
        if not os.path.exists(subdir):
            os.makedirs(subdir)

    def _writejson(self, _key, _value, index):
        typedir = subdir + os.sep + \
            str(index) + os.sep + _value['typeinfo']['type']
        self._mkdir(typedir)

        with open(os.path.join(typedir, _key + '.json'), 'w', encoding='latin1') as ff:
            json.dump(_value, ff, sort_keys=True,
                      indent=4, separators=(',', ': '))

    def _readRawData(self):
        with open(self.path, 'rb') as f:
            gpd = f.read()
        gpd = struct.pack('B' * len(gpd), *gpd[::-1])
        gpd = zlib.decompress(gpd)
        gpd = pickle.loads(gpd, encoding='latin1')
        return gpd

    def decode(self):
        gpd = self._readRawData()
        for index, elem in enumerate(gpd):
            if not isinstance(elem, dict):
                continue

            with open('GameParams-' + str(index) + '.json', 'w', encoding='latin1') as ff:
                json.dump(elem, ff, cls=GPEncode, sort_keys=True,
                          indent=4, separators=(',', ': '))

    def split(self):
        gpd = self._readRawData()

        subdir = 'split'
        self._mkdir(subdir)

        for index, elem in enumerate(gpd):
            if not isinstance(elem, dict):
                continue

            elemjson = json.dumps(elem, cls=GPEncode, ensure_ascii=False)
            elemjson = json.loads(elemjson)

            with ThreadPoolExecutor() as tpe:
                tpe.map(lambda p: writejson(*p), [(k, v, index)
                        for k, v in elemjson.items()])


if __name__ == '__main__':
    gp = WoWsGameParams('GameParams.data')
    gp.decode()
    gp.split()
