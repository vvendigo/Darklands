# based upon Olemar's info
import os
from struct import unpack


class EnemyPalette:
    def __init__(self):
        self.start_index = 0
        self.data = []
        self.extra = []

    def from_data(self, data):
        self.start_index = unpack('B', data[0:1])[0] / 3
        pos = 1
        for _ in range(0, 16):
            r, g, b = [x*4 for x in unpack('BBB', data[pos:pos+3])]
            self.data.append((r, g, b))
            pos += 3
        self.extra = unpack('BBBB', data[pos:pos+4])

    def get_dict(self):
        res = {}
        for i, c in enumerate(self.data):
            res[self.start_index + i] = c
        return res

def read_palettes(fname):
    data = open(fname).read()
    dataLen = len(data)
    pals = []
    pos = 0
    pal_len = 1 + 3*16 + 4
    while pos < dataLen:
        pal = EnemyPalette()
        pal.from_data(data[pos:pos+pal_len])
        pos += pal_len
        pals.append(pal)
    return pals

def readData(dlPath):
    fname = os.path.join(dlPath, 'ENEMYPAL.DAT')
    return read_palettes(fname)


# main ------------
if __name__ == '__main__':
    import sys
    from utils import itemStr

    dlPath = sys.argv[1] if len(sys.argv) > 1 else 'DL'

    pals = readData(dlPath)

    for i, pal in enumerate(pals):
        print('%2d: %s'%(i, pal.extra))

    print(pals[0].get_dict())
