import struct
import zlib
import pickle
import json
import os

class GPEncode(json.JSONEncoder):
    def default(self, o):
        try:
            for e in ['Cameras', 'DockCamera', 'damageDistribution', 'salvoParams']:
                o.__dict__.pop(e, o.__dict__)
            return o.__dict__
        except AttributeError:
            return {}

with open('GameParams.data', 'rb') as f:
    gpd = f.read()
gpd = struct.pack('B' * len(gpd), *gpd[::-1])
gpd = zlib.decompress(gpd)
gpd = pickle.loads(gpd, encoding='latin1')

for index, elem in enumerate(gpd):
    if not isinstance(elem, dict):
        continue

    with open('GameParams-' + str(index) + '.json', 'w', encoding='latin1') as ff:
        json.dump(elem, ff, cls=GPEncode, sort_keys=True, indent=4, separators=(',', ': '))
