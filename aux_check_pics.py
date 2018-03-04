
import glob


def checkPic(fname):
    data = [ord(c) for c in open(fname).read()]
    dataLen = len(data)
    print fname, dataLen,
    pos = 0
    while pos < dataLen:
        tag = (data[pos+1] << 8) | data[pos]
        pos += 2
        segLen = (data[pos+1] << 8) | data[pos]
        pos += 2
        #print hex(tag), segLen
        if tag == 0x304D: print 'P',
        elif tag == 0x3058:
            print 'I', (data[pos+1] << 8) | data[pos], 'x', (data[pos+3] << 8) | data[pos+2],
        else: print 'Unknown!',
        pos += segLen
    print

for f in glob.glob('DL/pics/*.pic'):
    checkPic(f)
