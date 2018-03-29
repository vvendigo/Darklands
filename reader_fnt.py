from utils import bread, sread

def readData(dlPath):
    fname = dlPath + '/fonts.fnt'

    data = map(ord, open(fname).read())
    dataLen = len(data)
    #print fname, dataLen, 'B'
    pos = 0

    cnt = bread(data[pos:pos+2]) ; pos += 2
    #print cnt, bread(data[pos:pos+1])
    offsets = []
    for i in xrange(0, cnt):
        offsets.append(bread(data[pos:pos+2])) ; pos += 2

    print offsets
    fonts = []

    # 0: ???
    # 1: len 776 b, start cca. (20*776+36)/8.0,  chars: 97
    # 2: len 1552 b, start cca. (15*1552+600)/8.0, chars 97, zero interlaced

    return fonts


# main ------------
if __name__ == '__main__':
    import sys
    from utils import itemStr

    dlPath = sys.argv[1] if len(sys.argv) > 1 else 'DL'

    fnts = readData(dlPath)

