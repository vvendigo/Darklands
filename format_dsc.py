import os
from struct import unpack
from utils import cstrim

def read_file(fname):
    data = open(fname).read()
    data_len = len(data)
    pos = 0
    unknown, = unpack('B', data[pos:pos+1]) ; pos += 1
    descs = []
    while pos < data_len:
        descs.append(cstrim(unpack('80s', data[pos:pos+80])[0])) ; pos += 80
    return descs

def readData(dlpath):
	return read_file(os.path.join(dlpath, 'darkland.dsc'))

# main ------------
if __name__ == '__main__':
    import sys

    dlPath = sys.argv[1] if len(sys.argv) > 1 else 'DL'

    descs = readData(dlPath)

    # print data
    for i, d in enumerate(descs):
        print(i, d)
