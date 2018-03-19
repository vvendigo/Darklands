from utils import bread

def dumpb(data):
    for i in xrange(0, len(data), 16):
        print ' '.join([("%2s"%hex(b)[2:].upper()).replace(' ', '0') for b in data[i:i+16]])

def readData(fname):
    data = map(ord, open(fname).read())
    dLen = len(data)
    out = []

    pos = 0
    fc = 0
    flags = 0
    while pos+2 < dLen:
        flags = (bread(data[pos:pos+2]) << fc) | flags
        pos += 2
        fc += 16
        while 1:
            if fc - 1 <= 0:
                break
            #print "%20s %2d |"%(("%20s"%bin(flags)[2:]).replace(' ','0')[-fc:], fc), ' ', len(out), '/', pos
            #dumpb(out)
            #print
            f = flags & 1 ; flags >>= 1 ; fc -= 1
            if f: # just copy next B
                out.append(data[pos]) ; pos += 1
            else: # things get complicated
                if fc - 1 <= 0:
                    flags = flags << 1
                    fc += 1
                    break
                f = flags & 1 ; flags >>= 1 ; fc -= 1
                seqLength, seqStart = None, None
                if not f: # 00 - yet simple
                    if fc - 1 < 2:
                        flags = flags << 2
                        fc += 2
                        break
                    # next 2 b from flags reversed = seqLength - 2
                    f = flags & 1 ; flags >>= 1 ; fc -= 1
                    seqLength = f << 1
                    f = flags & 1 ; flags >>= 1 ; fc -= 1
                    seqLength += f
                    seqLength += 2
                    # seqStart = 255 - next B
                    seqStart = 0xFF - data[pos] ; pos += 1
                else: # 01 - and more complicated
                    w = bread(data[pos:pos+2]) ; pos += 2
                    seqStart = (((w >> (8 + 3)) | 0xE0) << 8) | (w & 0xFF)
                    seqStart = 0xFFFF - seqStart
                    seqLength = (w >> 8) & 0x07
                    if seqLength > 0:
                        seqLength += 2
                    else:
                        b = data[pos] ; pos += 1
                        if b > 1:
                            seqLength = b
                            seqLength += 1
                        else:
                            # DONE!!!
                            # side effect - dummy 00FF00 at the end of file
                            #print pos
                            break

                # start left of output end
                seqStart = len(out) - seqStart - 1
                #print 'start', seqStart, '/', len(out), 'len', seqLength
                for i in xrange(0, seqLength):
                    out.append(out[seqStart+i])
                #if len(out) > 5*16: pos = dLen ; break;
    return out


def extractToFile(inPath, outPath):
    data = readData(inPath)
    fh = open(outPath, "wb")
    for b in data: fh.write(chr(b))
    fh.close()


# main ------------
if __name__ == '__main__':
    import sys

    filePath = sys.argv[1] # file to read
    if len(sys.argv) > 2:
        outFilePath = sys.argv[2] # file to write
        extractToFile(filePath, outFilePath)
    else:
        data = readData(filePath)
        dumpb(data)
        #print len(data)

