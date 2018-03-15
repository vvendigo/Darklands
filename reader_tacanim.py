from utils import sread


def readData(dlPath):
    fname = dlPath + '/tacanim.db'
    data = map(ord, open(fname).read())
    dataLen = len(data)

    tacanim = {}
    pos = 0
    while pos < dataLen:
        charCode = sread(data[pos:pos+4]) ; pos += 4
        tacanim[charCode] = data[pos:pos+10] ; pos += 10
        # last four bytes looks like 2 times width, depth for walk & combat??
        # Nope? :( change of last 4 bytes has no effect in battle

    return {'tacanim': tacanim}


# main ------------
if __name__ == '__main__':
    import sys
    from utils import itemStr

    dlPath = sys.argv[1] if len(sys.argv) > 1 else 'DL'

    data = readData(dlPath)

    for k in sorted(data['tacanim'].keys()):
        d = data['tacanim'][k]
        print '%3s: %s'%(k, (' '.join(['%3d']*10))%tuple(d))


