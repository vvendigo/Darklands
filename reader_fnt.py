import os
from utils import bread, sread

def readFonts(fname):
    data = map(ord, open(fname).read())
    dataLen = len(data)
    #print fname, dataLen, 'B'
    pos = 0

    cnt = bread(data[pos:pos+2]) ; pos += 2
    #print cnt, bread(data[pos:pos+1])
    offsets = []
    for i in xrange(0, cnt):
        offsets.append(bread(data[pos:pos+2])) ; pos += 2

    #print offsets
    fonts = []
    for off in offsets:
        # charset header
        hdrpos = off - 8
        startChr = data[hdrpos] # first char ASCII code
        endChr = data[hdrpos+1] # last char ASCII code
        bw = data[hdrpos+2] # width in bytes
        # 0 unknown
        bh = data[hdrpos+4] # height in bytes
        # 1 unknown
        # 1 unknown
        # 0 unknown
        charCnt = endChr - startChr + 1
        font = {'startChar': startChr, 'endChar': endChr, 'height': bh, 'chars':[]}
        chars = font['chars']
        widthOff = off - charCnt - 8
        for i in xrange(0, charCnt):
            chWidth = data[widthOff+i]
            char = {'width':chWidth, 'lines':[]}
            for j in xrange(0, bh):
                x = 0
                lnData = [0]*chWidth
                for k in xrange(0,bw):
                    lnB = data[off+(j*charCnt+i)*bw+k]
                    for bc in xrange(0,8):
                        if x >= chWidth: break
                        lnData[x] = 1 if lnB & 0x80 else 0
                        x += 1
                        lnB <<= 1
                char['lines'].append(lnData)
            chars.append(char)
        fonts.append(font)
    return fonts


def readData(dlPath):
    fonts = {}
    for ext in ('fnt', 'utl'):
        fname = os.path.join(dlPath, 'fonts.') + ext
        fonts[ext] = readFonts(fname)
    return fonts


# main ------------
if __name__ == '__main__':
    import sys
    from utils import itemStr

    dlPath = sys.argv[1] if len(sys.argv) > 1 else 'DL'

    fonts = readData(dlPath)

    for ext, fnts in fonts.iteritems():
        print '------', ext
        for i,fnt in enumerate(fnts):
            print "-----", i, 'h:', fnt['height']
            chC = fnt['startChar']
            for ch in fnt['chars']:
                print 'ch: %d, w: %d'%(chC, ch['width'])
                chC += 1
                for r in ch['lines']:
                    print ''.join([('.','#')[b] for b in r])
                print
            print

