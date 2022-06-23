import struct
import zlib
import pickle
import json
import os
from concurrent.futures import ThreadPoolExecutor

class GPEncode(json.JSONEncoder):
    def default(self, o):
        try:
            for e in ['Cameras', 'DockCamera', 'damageDistribution', 'salvoParams']:
                o.__dict__.pop(e, o.__dict__)
            return o.__dict__
        except AttributeError:
            return {}

def mkdir(subdir):
    if not os.path.exists(subdir):
        os.makedirs(subdir)

def writejson(_key, _value, index):
    typedir = subdir + os.sep + str(index) + os.sep + _value['typeinfo']['type']
    mkdir(typedir)

    with open(os.path.join(typedir, _key + '.json'), 'w', encoding='latin1') as ff:
        json.dump(_value, ff, sort_keys=True, indent=4, separators=(',', ': '))

with open('GameParams.data', 'rb') as f:
    gpd = f.read()
gpd = struct.pack('B' * len(gpd), *gpd[::-1])
gpd = zlib.decompress(gpd)
gpd = pickle.loads(gpd, encoding='latin1')

subdir = 'split'
mkdir(subdir)

for index, elem in enumerate(gpd):
    if not isinstance(elem, dict):
        continue

    elemjson = json.dumps(elem, cls=GPEncode, ensure_ascii=False)
    elemjson = json.loads(elemjson)

    with ThreadPoolExecutor() as tpe:
        tpe.map(lambda p: writejson(*p), [(k, v, index) for k, v in elemjson.items()])
