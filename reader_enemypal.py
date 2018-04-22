# based upon Olemar's info

def readData(dlPath):
    fname = dlPath + '/enemypal.dat'
    data = map(ord, open(fname).read())
    dataLen = len(data)

    pals = []
    pos = 0
    while pos < dataLen:
        pal = {}
        startIdx = data[pos]/3
        pal['start'] = startIdx
        pos += 1
        for i in xrange(startIdx, startIdx+16):
            pal[i] = (data[pos]*4, data[pos+1]*4, data[pos+2]*4)
            pos += 3
        pal['extra'] = data[pos:pos+4]
        pos += 4
        pals.append(pal)
    return pals


# main ------------
if __name__ == '__main__':
    import sys
    from utils import itemStr

    dlPath = sys.argv[1] if len(sys.argv) > 1 else 'DL'

    data = readData(dlPath)

    for i, pal in enumerate(data):
        print '%2d: %s'%(i, pal['extra'])

