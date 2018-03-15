from utils import sread


def readData(fname):
    data = map(ord, open(fname).read())
    dataLen = len(data)

    ptrs = []
    pos = 0
    lastVal = 0
    while pos < dataLen:
        if lastVal == 0xff and data[pos] == 0xff:
            ptrs.append(pos+1)
        lastVal = data[pos]
        pos += 1

    out = []
    lastP = 0
    for p in ptrs:
        out.append(data[lastP:p])
        lastP = p

    b2 = []
    for b in data[lastP:]:
        b2.append(b>>4)
        b2.append(b&0xf)

    out.append(b2)

    print dataLen-lastP, ptrs

    return out


# main ------------
if __name__ == '__main__':
    import sys
    from utils import itemStr

    fname = sys.argv[1]

    data = readData(fname)

    for d in data[:-1]:
        print d

    '''
    for i in xrange(8,16):
        for j, d in enumerate(data[-1]):
            print "%2d"%d,
            if j % i == 0:
                print
        print
    '''
    print
